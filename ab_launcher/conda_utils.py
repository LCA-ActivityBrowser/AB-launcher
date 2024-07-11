import os
import sys

from ab_launcher import paths
from conda.misc import (
    CondaExitZero,
    DryRunExit,
    MatchSpec,
    PackageCacheData,
    ParseError,
    PrefixData,
    PrefixSetup,
    ProgressiveFetchExtract,
    UnlinkLinkTransaction,
    context,
    defaultdict,
    expand,
    is_url,
    join_url,
    path_to_url,
    url_pat,
)
from conda.base import constants

# set conda context
context.always_copy = True
context.safety_checks = constants.SafetyChecks.disabled


def explicit_updater(specs, notifier, prefix=paths.ENV_DIR):
    actions = defaultdict(list)
    actions["PREFIX"] = prefix

    fetch_specs = []
    for spec in specs:
        if spec == "@EXPLICIT":
            continue

        if not is_url(spec):
            """
            # This does not work because url_to_path does not enforce Windows
            # backslashes. Should it? Seems like a dangerous change to make but
            # it would be cleaner.
            expanded = expand(spec)
            urled = path_to_url(expanded)
            pathed = url_to_path(urled)
            assert pathed == expanded
            """
            spec = path_to_url(expand(spec))

        # parse URL
        m = url_pat.match(spec)
        if m is None:
            raise ParseError(f"Could not parse explicit URL: {spec}")
        url_p, fn, md5sum = m.group("url_p"), m.group("fn"), m.group("md5")
        url = join_url(url_p, fn)
        # url_p is everything but the tarball_basename and the md5sum

        fetch_specs.append(MatchSpec(url, md5=md5sum) if md5sum else MatchSpec(url))

    if context.dry_run:
        raise DryRunExit()

    pfe = ProgressiveFetchExtract(fetch_specs)
    notifier.notify("Downloading packages...", False)
    pfe.execute()

    if context.download_only:
        raise CondaExitZero(
            "Package caches prepared. "
            "UnlinkLinkTransaction cancelled with --download-only option."
        )

    # now make an UnlinkLinkTransaction with the PackageCacheRecords as inputs
    # need to add package name to fetch_specs so that history parsing keeps track of them correctly
    specs_pcrecs = tuple(
        [spec, next(PackageCacheData.query_all(spec), None)] for spec in fetch_specs
    )

    # Assert that every spec has a PackageCacheRecord
    specs_with_missing_pcrecs = [
        str(spec) for spec, pcrec in specs_pcrecs if pcrec is None
    ]
    if specs_with_missing_pcrecs:
        if len(specs_with_missing_pcrecs) == len(specs_pcrecs):
            raise AssertionError("No package cache records found")
        else:
            missing_precs_list = ", ".join(specs_with_missing_pcrecs)
            raise AssertionError(
                f"Missing package cache records for: {missing_precs_list}"
            )

    precs_to_remove = []
    prefix_data = PrefixData(prefix)
    installed = {rec.name for rec in prefix_data.iter_records()}

    for q, (spec, pcrec) in enumerate(specs_pcrecs):
        new_spec = MatchSpec(spec, name=pcrec.name)
        specs_pcrecs[q][0] = new_spec

        #prec = prefix_data.get(pcrec.name, None)
        if pcrec.name in installed:
            installed.remove(pcrec.name)
            # if it matches the exact spec, don't relink
            if next(prefix_data.query(new_spec), None):
                specs_pcrecs[q][0] = None

            # if it is another spec, unlink the old spec
            else:
                precs_to_remove.append(prefix_data.get(pcrec.name, None))

    leftover_precs = [prefix_data.get(rec_name, None) for rec_name in installed]
    precs_to_remove.extend(leftover_precs)

    stp = PrefixSetup(
        prefix,
        precs_to_remove,
        tuple(sp[1] for sp in specs_pcrecs if sp[0]),
        (),
        tuple(sp[0] for sp in specs_pcrecs if sp[0]),
        (),
    )

    txn = NotifiedUnlinkLinkTransaction(notifier, stp)
    if not context.json and not context.quiet:
        txn.print_transaction_summary()

    txn.prepare()
    txn.verify()
    txn.execute()


class NotifiedUnlinkLinkTransaction(UnlinkLinkTransaction):
    def __init__(self, notifier, *args):
        super().__init__(*args)
        self.notifier = notifier

    def prepare(self):
        self.notifier.notify("Preparing transaction...", False)
        super().prepare()

    def verify(self):
        self.notifier.notify("Verifying transaction...", False)
        super().verify()

    def execute(self):
        self.notifier.notify("Executing transaction...", False)
        super().execute()


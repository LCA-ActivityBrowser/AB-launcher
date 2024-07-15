from ab_launcher import paths
from .linking import conda_create  # needed for patching
import conda.misc as conda_misc
from conda.base import constants


# set conda context
conda_misc.context.always_copy = True
conda_misc.context.safety_checks = constants.SafetyChecks.disabled


def parse_specs(spec_list) -> [conda_misc.MatchSpec]:
    specs = []

    for spec in spec_list:
        m = conda_misc.url_pat.match(spec)
        url_p, fn = m.group("url_p"), m.group("fn")
        url = conda_misc.join_url(url_p, fn)
        specs.append(conda_misc.MatchSpec(url))

    return specs


def explicit_updater(spec_list, notifier, prefix=paths.ENV_DIR):
    prefix_data = conda_misc.PrefixData(prefix)

    specs = parse_specs(spec_list)

    # download packages missing from the environment
    notifier.notify("Downloading packages...", False)
    missing_specs = tuple([spec for spec in specs if not next(prefix_data.query(spec), False)])
    conda_misc.ProgressiveFetchExtract(missing_specs).execute()
    new_packages = tuple(next(conda_misc.PackageCacheData.query_all(spec)) for spec in missing_specs)

    # find any packages that are obsolete
    spec_set = {match_spec.fn for match_spec in specs}
    obsolete_packages = [rec for rec in prefix_data.iter_records() if rec.fn not in spec_set]

    setup = conda_misc.PrefixSetup(
        target_prefix=prefix,
        unlink_precs=obsolete_packages,
        link_precs=new_packages,
        remove_specs=(),
        update_specs=(),
        neutered_specs=(),
    )

    txn = NotifiedUnlinkLinkTransaction(notifier, setup)
    txn.print_transaction_summary()

    txn.prepare()
    txn.verify()
    txn.execute()


class NotifiedUnlinkLinkTransaction(conda_misc.UnlinkLinkTransaction):
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


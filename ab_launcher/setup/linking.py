import shutil
import conda.gateways.disk.create as conda_create

import ab_launcher.paths


def create_link(src, dst, link_type, force=False):
    if link_type == conda_create.LinkType.directory:
        # A directory is technically not a link.  So link_type is a misnomer.
        #   Naming is hard.
        if conda_create.lexists(dst) and not conda_create.isdir(dst):
            conda_create.rm_rf(dst)
        conda_create.mkdir_p(dst)
        return

    if ab_launcher.paths.PKGS_DIR not in src and ab_launcher.paths.ENV_DIR not in src:
        return

    shutil.move(src, dst)
    return


conda_create.create_link = create_link

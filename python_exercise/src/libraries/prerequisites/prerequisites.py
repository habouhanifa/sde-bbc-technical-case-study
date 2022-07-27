from libraries.utils.gcs_utils import GCSHelper
from libraries.utils.utils import Loggable


class RunPrerequisites(Loggable):

    def __init__(self):
        super().__init__()
        self.gcs_helper = GCSHelper()

    def make_bucket_public(self):
        self.gcs_helper.set_bucket_public_iam()


if __name__ == '__main__':
    rp = RunPrerequisites()
    rp.make_bucket_public()

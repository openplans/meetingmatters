from django.core.management.base import BaseCommand, CommandError
import os
import subprocess

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        static_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'static')
        )

        assert os.path.exists(static_dir)

        params = dict(
            infile = os.path.join(static_dir, 'less', 'publicmeeting.less'),
            outfile = os.path.join(static_dir, 'css', 'publicmeeting.css'),
            bootstrap_dir = os.path.join(static_dir, '..', '..', '..', 'env/lib/python2.7/site-packages/bootstrapped/static/less/')
        )

        assert os.path.exists(params['bootstrap_dir'])

        subprocess.call(
            ["lessc",
             "{infile}".format(**params),
             "{outfile}".format(**params),
             "-I{bootstrap_dir}".format(**params)],
            stdout=self.stdout,
            stderr=self.stderr
        )

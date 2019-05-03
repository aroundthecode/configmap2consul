import schedule
import time
import click

from configmap2consul.configmap2consul import configmap_2_consul, logging, init_consul_client

log = logging.getLogger("cli")
log_format = "%(asctime)s | %(levelname)9s | %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)

CLICK_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CLICK_CONTEXT_SETTINGS)
@click.option('--namespace', '-n',
              required=True,
              type=str,
              default="default",
              help='Kubernetes Configmap Namespace')
@click.option('--interval', '-i',
              required=True,
              type=int,
              default=5,
              show_default=True,
              help="Polling interval, if -1 will run once and quit")
@click.option('--labels', '-l',
              required=False,
              type=str,
              help="Labels to filter kubernetes configmap")
@click.option('--consul_url', '-c',
              required=True,
              type=str,
              default="http://localhost:8500",
              help="Consul endpoint: e.g https://myconsul.mydomain.org:8500")
@click.option('--basepath', '-p',
              required=True,
              type=str,
              default="test",
              help="Consul path for stored K/V")
@click.option('--mode', '-m',
              required=True,
              type=str,
              default="basic",
              help="Write mode, currently supports 'basic' and 'spring'")
@click.option('--separator', '-s',
              required=False,
              default="::",
              type=str,
              help="token separator for profile version (spring mode only)")
@click.option("--dryrun", "-d",
              is_flag=True,
              help="Do not create consul data")
def main(namespace=None, interval=None, labels=None, consul_url=None, basepath=None, mode=None, separator=None, dryrun=None):

    consul_client = init_consul_client(consul_url)

    if interval == -1:
        log.info("Single run mode")
        configmap_2_consul(
            namespace,
            labels,
            consul_client,
            basepath,
            mode,
            separator,
            dryrun)

    else:
        log.info("Scheduled run mode")
        # run first
        configmap_2_consul(
            namespace,
            labels,
            consul_client,
            basepath,
            mode,
            separator,
            dryrun)

        # schedule next
        schedule.every(interval).seconds.do(
            configmap_2_consul,
            namespace,
            labels,
            consul_client,
            basepath,
            mode,
            separator,
            dryrun)

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    main()

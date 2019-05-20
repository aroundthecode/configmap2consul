import configmap2consul.cli
from click.testing import CliRunner


def test_cli_help():

    runner = CliRunner()
    result = runner.invoke(configmap2consul.cli.main, '-h')
    assert result.exit_code == 0
    assert "--namespace" in result.output


def test_cli_dry():
    runner = CliRunner()
    result = runner.invoke(configmap2consul.cli.main, '-d -i -1')
    assert result.exit_code == 0

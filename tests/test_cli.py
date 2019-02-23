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


def test_cli_basic():
    runner = CliRunner()
    result = runner.invoke(
        configmap2consul.cli.main,
        '-m basic -c http://192.168.99.100:32080 -i -1'
    )
    assert result.exit_code == 0


def test_cli_spring():
    runner = CliRunner()
    result = runner.invoke(
        configmap2consul.cli.main,
        '-m spring -l mode=spring -c http://192.168.99.100:32080 -i -1'
    )
    assert result.exit_code == 0


def test_cli_labelsel():
    runner = CliRunner()
    result = runner.invoke(
        configmap2consul.cli.main,
        '-m spring -l configmap2consul=True -c http://192.168.99.100:32080 -i -1'
    )
    assert result.exit_code == 0

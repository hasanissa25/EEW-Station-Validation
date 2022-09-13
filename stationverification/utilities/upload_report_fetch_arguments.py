import argparse
from stationverification.config import get_default_parameters


class UserInput(dict):
    @property
    def projectId(self) -> int:
        return self["projectId"]

    @property
    def wikiTitle(self) -> str:
        return self["wikiTitle"]

    @property
    def projectToken(self) -> str:
        return self["projectToken"]

    @property
    def gitlabUrl(self) -> str:
        return self["gitlabUrl"]

    @property
    def webServer(self) -> str:
        return self["webServer"]

    @property
    def typeofinstrument(self) -> str:
        return self["typeofinstrument"]


def upload_report_fetch_arguments() -> UserInput:
    argsparser = argparse.ArgumentParser()
    argsparser.add_argument(
        "-i",
        "--projectId",
        help="Project ID of GitLab project. Ex: 10",
        type=int,
    )
    argsparser.add_argument(
        "-t",
        "--wikiTitle",
        help="Title of wiki page. Ex: 'QW.QCC01'",
        type=str,
        required=True
    )
    argsparser.add_argument(
        "-T",
        "--projectToken",
        help="Project token. Ex: WJgJ8NZDP2ei_KpiF8s8",
        type=str,
    )
    argsparser.add_argument(
        "-u",
        "--gitlabUrl",
        help='URL of GitLab project. Ex: "http://gitlab.seismo.nrcan.gc.ca"',
        type=str,
    )
    argsparser.add_argument(
        "-w",
        "--webServer",
        help='Path to the validation result files. \
Ex: "http://3.96.234.48:18010/QW/ONE01/2022-04-21-2022-05-01/"',
        type=str,
        required=True
    )
    argsparser.add_argument(
        "-I",
        "--typeofinstrument",
        help='Type of instrument. Either Fortimus, or Nanometrics',
        type=str,
        required=True
    )
    args = argsparser.parse_args()
    default_parameters = get_default_parameters()

    gitlabUrl = args.gitlabUrl if args.gitlabUrl is not None\
        else default_parameters.GITLAB_URL
    projectId = args.projectId if args.projectId is not None\
        else default_parameters.PROJECT_ID
    projectToken = default_parameters.PROJECT_TOKEN
    # webserver = args.webserver if args.webserver is not None\
    #     else default_parameters.WEB_SERVER
    webServer = args.webServer
    wikiTitle = args.wikiTitle
    typeofinstrument = args.typeofinstrument.lower()

    return UserInput(gitlabUrl=gitlabUrl,
                     projectId=projectId,
                     projectToken=projectToken,
                     webServer=webServer,
                     wikiTitle=wikiTitle,
                     typeofinstrument=typeofinstrument
                     )

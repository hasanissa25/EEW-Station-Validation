'''
Python script used to upload validation results to GitLab wikis.

usage: uploadreport

Functions:
----------
main()
    The main fuction, which takes care of calling the other functions
'''


# from stationverification.utilities.upload_report_fetch_arguments\
#  import upload_report_fetch_arguments


from stationverification.utilities.GitLabAttachments \
    import GitLabAttachments
from stationverification.utilities.GitLabWikis \
    import GitLabWikis
from stationverification.utilities.generate_markdown_template \
    import generate_markdown_template_for_full_validation, \
    generate_markdown_template_for_latency_validation
from stationverification.utilities.upload_report_fetch_arguments\
    import upload_report_fetch_arguments
import logging

logging.basicConfig(
    format='%(asctime)s Upload to GitLab: %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def main():
    user_input = upload_report_fetch_arguments()

    GitLabWikisObj = GitLabWikis(
        title=user_input.wikiTitle,
        gitlabUrl=user_input.gitlabUrl,
        projectId=user_input.projectId,
        token=user_input.projectToken,
        webserver=user_input.webServer)

    GitLabWikisObj.setup_wiki()

    GitLabAttachmentsObj = GitLabAttachments(
        list_of_attachments=GitLabWikisObj.list_of_attachment_references)
    attachments = GitLabAttachmentsObj.get_attachments()
    if not GitLabWikisObj.validation_json:
        content = generate_markdown_template_for_latency_validation(
            attachments=attachments)
    else:
        content = generate_markdown_template_for_full_validation(
            attachments=attachments,
            json_report=GitLabWikisObj.validation_json,
            typeofinstrument=user_input.typeofinstrument)
    GitLabWikisObj._post_wiki_api(content=content)

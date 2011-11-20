import utils

ignore = [
    'plonenext',
    ]

targets = [
    utils.github_list_repos_of_organisation('plone'),
    utils.github_list_repos_of_organisation('collective'),
    utils.svn_list_repos('svn://svn.zope.org/repos/main/'),
    ]


global baseurl
baseurl = 'http://svn.plone.org/svn/collective/'

def svn_list(subpath, ignore):
    url = baseurl + subpath
    return utils.filter_packages_by_name(
        lambda name: name not in ignore,
        utils.svn_list_repos(url))

packages = utils.merge_packages(
    svn_list('', ('simplelayout',)),
    svn_list('simplelayout', ()),
    )

utils.compare_packages(packages, targets)

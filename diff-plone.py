import utils

ignore = [
    'plonenext',
    ]

targets = [
    utils.github_list_repos_of_organisation('plone'),
    utils.github_list_repos_of_organisation('collective'),
    utils.svn_list_repos('svn://svn.zope.org/repos/main/'),
    ]

url = 'http://svn.plone.org/svn/plone'
packages = utils.filter_packages_by_name(
    lambda name: name.startswith('plone') and name not in ignore,
    utils.svn_list_repos(url))

utils.compare_packages(packages, targets, url)

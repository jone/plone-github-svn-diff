from xml.dom.minidom import parseString
import json
import shlex
import subprocess
import urllib


def todict(func):
    def _decorator(*args, **kwargs):
        return dict(func(*args, **kwargs))
    return _decorator


def tolist(func):
    def _decorator(*args, **kwargs):
        return list(func(*args, **kwargs))
    return _decorator


@todict
def github_list_repos_of_organisation(orgname):
    url = 'https://api.github.com/orgs/%s/repos' % orgname
    response = urllib.urlopen(url)
    assert response.getcode() == 200, 'request failed: %s, %s' % (
        response.getcode(), url)
    data = json.loads(response.read())
    for repo in data:
        yield repo['name'], repo['pushed_at']


@todict
def svn_list_repos(url):
    cmd = 'svn ls --xml %s' % url
    exitcode, stdout, stderr = _runcmd(cmd)
    assert exitcode == 0, 'Command failed: %s' % cmd

    getcontent = lambda elm: elm.childNodes[0].nodeValue

    doc = parseString(stdout)
    for entry in doc.getElementsByTagName('entry'):
        yield (getcontent(entry.getElementsByTagName('name')[0]),
               getcontent(entry.getElementsByTagName('date')[0]))


def compare_packages(packages, targets, prefixurl=''):
    if prefixurl:
        prefixurl = prefixurl.endswith('/') and prefixurl or prefixurl + '/'
    _printresult(_compare(packages, targets), prefixurl=prefixurl)


def filter_packages_by_name(name_filter, packages):
    packages = packages.items()
    packages = filter(lambda item: name_filter(item[0]), packages)
    return dict(packages)


def merge_packages(*lists):
    packages = {}
    for list_ in lists:
        packages.update(list_)
    return packages


@tolist
def _get_pypi_packages():
    url = 'http://pypi.python.org/simple/'
    response = urllib.urlopen(url)
    assert response.getcode() == 200, 'pypi request failed'

    doc = parseString(response.read())
    for link in doc.getElementsByTagName('a'):
        name = link.getAttribute('href')
        name = name.endswith('/') and name[:-1] or name
        yield name


def _compare(packages, targets):
    moved_packages = {}
    for data in targets:
        moved_packages.update(data)

    pypi = _get_pypi_packages()

    result = {'released': {},
              'notreleased': {}}

    for name, lastmodified in packages.items():
        if name in moved_packages:
            continue

        year = lastmodified[:4]
        if name in pypi:
            resultkey = 'released'
        else:
            resultkey = 'notreleased'

        if year not in result[resultkey]:
            result[resultkey][year] = set()

        result[resultkey][year].add(name)

    return result


def _printresult(result, prefixurl=''):
    print '# released on pypi'
    for year in reversed(sorted(result['released'].keys())):
        names = result['released'][year]
        print '##', year
        for name in sorted(names):
            print '-', prefixurl + name
        print ''

    print ''
    print '# not released on pypi'
    for year in reversed(sorted(result['notreleased'].keys())):
        names = result['notreleased'][year]
        print '##', year
        for name in sorted(names):
            print '-', prefixurl + name
        print ''


def _runcmd(cmd):
    proc = subprocess.Popen(shlex.split(cmd),
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    output, errors = proc.communicate()
    return proc.poll(), output, errors


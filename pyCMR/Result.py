'''
Copyright 2017, United States Government, as represented by the Administrator of the National Aeronautics and Space Administration. All rights reserved.

The pyCMR platform is licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

'''
import requests
import shutil
import urllib


class Result(dict):
    """
    The class to structure the response xml string from the cmr API
    """
    _location = None

    def download(self, destpath="."):
        """
        Download the dataset into file system
        :param destPath: use the current directory as default
        :return:
        """
        url = self._location
        # Downloadable url does not exist
        if not url:
            return None
        if url.startswith('ftp'):
            urllib.urlretrieve(url,destpath + "/" + self._downloadname.replace('/', '') )
        else:
            r = requests.get(url, stream=True)
            r.raw.decode_content = True

            with open(destpath + "/" + self._downloadname.replace('/', ''), 'wb') as f:
                shutil.copyfileobj(r.raw, f)

    def getDownloadUrl(self):
        """
        :return:
        """
        return self._location

class Collection(Result):
    def __init__(self, metaResult, cmr_host):
        for k in metaResult:
            self[k] = metaResult[k]

        self._location = 'https://{}/search/concepts/{}.umm-json'.format(cmr_host, metaResult['concept-id'])
        self._downloadname = metaResult['Collection']['ShortName']

class Granule(Result):
    def __init__(self, metaResult):

        for k in metaResult:
            self[k] = metaResult[k]

        # Retrieve downloadable url
        try:
            self._location = self['Granule']['OnlineAccessURLs']['OnlineAccessURL'][0]['URL']
            self._downloadname = self._location.split("/")[-1]
        except KeyError:
            self._location = None

        # Retrieve OPeNDAPUrl
        try:
            urls = self['Granule']['OnlineResources']['OnlineResource']
            self._OPeNDAPUrl = filter(lambda x: x["Type"] == "OPeNDAP", urls)[0]['URL']
        except :
            self._OPeNDAPUrl = None

    def getOPeNDAPUrl(self):
        return self._OPeNDAPUrl

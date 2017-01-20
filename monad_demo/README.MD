The need
Currently we are lacking the flexibility of manipulating input json format pod config.
By that we meant not only can't we create a json format file contains the proper keys
for oc-tools modules to use easily(ref_1) , but also we have to do lot's of self.getdictobj (ref_2),
which by each call will loop the pod config json again and again to get the proper key.
After that, we do the validation, and then to aggregate the key to create the proper dict for each
task/oc-tool module to use.
When new requirements arrive, we do the above steps again by writing redundant code.
The proposal is to give a solution base on the concept of monad to generate needed
pod config in a most simple way.
Explain with examples
Here we'll try to explain the usage by examples.
This install_json.json file will be used through out the examples:
http://10.250.90.37:5566/source/xref/monad_demo/install_json.json
Example 1
Extract siteconf out of install_json.json.
By default we have a validator installed to check for value's emptiness.
We need 1 line of code to do the extraction, with build-in validation:
http://10.250.90.37:5566/source/xref/monad_demo/main.py#59
 
site_conf = key_monad("install_json/siteconf", j)

Here's the result:
http://10.250.90.37:5566/source/xref/monad_demo/example_1
While key:
[u'/siteconf/network/clusters/10.252.196.129/26/dhcpstart']
is invalid due to it's emptiness, we can verify that in our install_json.json:
http://10.250.90.37:5566/source/xref/monad_demo/install_json.json#178
 
Example 2
Extract siteconf and install_json , 2 key values out of install_json.json
First we create a monad with key 'install_json/siteconf',
http://10.250.90.37:5566/source/xref/monad_demo/main.py#69
 
site_conf = key_monad("install_json/siteconf", j)

Then we create another monad with key 'install_json'.
http://10.250.90.37:5566/source/xref/monad_demo/main.py#70
 
install_json = key_monad("install_json", j)

And simply aggregate them while we get the aggregated monad:
http://10.250.90.37:5566/source/xref/monad_demo/main.py#71
result = site_conf.apply(install_json)
Here's the result:
http://10.250.90.37:5566/source/xref/monad_demo/example_2

Example 3
Let's generate oc-install-gateway needed json file.
Those are the keys that we needed:
http://10.250.90.37:5566/source/xref/monad_demo/main.py#11
GATEWAY_KEY = (
    'install_json/default_ilom_user',
    'install_json/default_ilom_password',
    'install_json/controlplane_subnet',
    'install_json/site_name',
    'install_json/seed_ilom',
    'install_json/seed_gateway',
    'install_json/seed_ip_addr',
    'install_json/root_user',
    'install_json/root_password',
    'install_json/external_dns',
    'install_json/nodeuser',
    'gateway/gateway_node_iloms')
And we simply aggregate them:
http://10.250.90.37:5566/source/xref/monad_demo/main.py#81
gateway = generate_config(j, GATEWAY_KEY)
Here's the result:
http://10.250.90.37:5566/source/xref/monad_demo/example_3

Example 4
What if after we have the gateway json file ready, but we need one more
extra key later on out of install_json.json for the newer oc-install-gateway version,
say, we need 'nfs_location' key.

Easy, monads can be associated.
First we create a nfs_location monad:
http://10.250.90.37:5566/source/xref/monad_demo/main.py#92
 
nfs_location = key_monad("nfs_location", j)

Then aggregate with previous gateway moand:
http://10.250.90.37:5566/source/xref/monad_demo/main.py#93
 
result = nfs_location.apply(gateway)
Tada, here's the result:
http://10.250.90.37:5566/source/xref/monad_demo/example_4

Example 5
What if we create a monad which it's key doesn't exist in install_json.json?
Well, in this case, the context of the monad will be None.
It won't throw exception, but will be show in the invalid key list since it's empty.
Here's the example, creating a none exist key monad:
http://10.250.90.37:5566/source/xref/monad_demo/main.py#105
 
not_exist = key_monad("not_exist/hahaha", j)

Here's the result:
http://10.250.90.37:5566/source/xref/monad_demo/example_5
As we can see, 'hahaha' is in the invalid key list.

Example 6
What if we accidentally aggregate same key multiple times?
For that will create the same monad with single key value, which is
valid for export into json.
http://10.250.90.37:5566/source/xref/monad_demo/main.py#117
 
nfs_location_1 = key_monad("nfs_location", j)
nfs_location_2 = key_monad("nfs_location", j)
result = nfs_location_1.apply(nfs_location_2)

Here's the result:
http://10.250.90.37:5566/source/xref/monad_demo/example_6

Example 7
Install our own validator.
Now we install our own validator to check key 'nfs_location' has value contains
'iso'.
http://10.250.90.37:5566/source/xref/monad_demo/main.py#129
 
def check_has_iso(key, result):
        if key == "nfs_location":
            if "iso" in result[key]:
                return []
            else:
                return [key]

Here's the result:
http://10.250.90.37:5566/source/xref/monad_demo/example_7
We could see the ['nfs_location'] is invalid since it does not have 'iso' substring.

Future work
Using FP's foldr to create a list of validator for validating the key/value.
 
Reference
ref_1:
we have add cluster:
http://10.250.90.37:5566/source/xref/compute-konrad-deployer_Master/deployer/compute/tasks/operate/expand_tasks.py#74
install_json:
http://10.250.90.37:5566/source/xref/compute-konrad-deployer_Master/deployer/compute/tasks/create/create_tasks.py#86
And later on we'll have racdb json and gateway json.
ref_2:
http://10.250.90.37:5566/source/xref/compute-konrad-deployer_Master/deployer/compute/lib/config.py#571
if do a quick search, there are 35 calls to self.getdictobj
and each call will do a dict search...
Monad
http://mvanier.livejournal.com/3917.html

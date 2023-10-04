"""This is a trivial example of a gitrepo-based profile; The profile source code and other software, documentation, etc. are stored in in a publicly accessible GIT repository (say, github.com). When you instantiate this profile, the repository is cloned to all of the nodes in your experiment, to `/local/repository`. 

This particular profile is a simple example of using a single raw PC. It can be instantiated on any cluster; the node will boot the default operating system, which is typically a recent version of Ubuntu.

Instructions:
Wait for the profile instance to start, then click on the node in the topology and choose the `shell` menu item. 
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()
 
# Add a raw PC to the request.
node = request.RawPC("node")

# Allocate a node and ask for a 30GB file system mounted at /mydata
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU16-64-STD"
bs = node.Blockstore("bs", "/mydata")
bs.size = "30GB"

# Install and execute a script that is contained in the repository.
node.addService(pg.Execute(shell="sh", command="/local/repository/silly.sh"))


# TESTING SETTING PARAMETERS

# Describe the parameter(s) this profile script can accept.
portal.context.defineParameter( "n", "Number of VMs", portal.ParameterType.INTEGER, 1 )

# Retrieve the values the user specifies during instantiation.
params = portal.context.bindParameters()

# Create a Request object to start building the RSpec.
request = portal.context.makeRequestRSpec()

# Check parameter validity.
if params.n < 1 or params.n > 8:
    portal.context.reportError( portal.ParameterError( "You must choose at least 1 and no more than 8 VMs.", ["n"] ) )

# Abort execution if there are any errors, and report them.
portal.context.verifyParameters()


# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)

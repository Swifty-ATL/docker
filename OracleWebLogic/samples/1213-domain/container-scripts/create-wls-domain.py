# WebLogic on Docker Default Domain
#
# Default domain 'base_domain' to be created inside the Docker image for WLS
# 
# Since : October, 2014
# Author: bruno.borges@oracle.com
# ==============================================
admin_port = int(os.environ.get("ADMIN_PORT", "8001"))
admin_pass = os.environ.get("ADMIN_PASSWORD", "welcome1")

# Open default domain template
# ======================
readTemplate("/u01/oracle/weblogic/wlserver/common/templates/wls/wls.jar")

# Disable Admin Console
# --------------------
# cmo.setConsoleEnabled(false)

# Configure the Administration Server and SSL port.
# =========================================================
cd('Servers/AdminServer')
set('ListenAddress','')
set('ListenPort', admin_port)

# Define the user password for weblogic
# =====================================
cd('/')
cd('Security/base_domain/User/weblogic')
cmo.setPassword(admin_pass)

# Create a JMS Server
# ===================
#cd('/')
#create('myJMSServer', 'JMSServer')

# Create a JMS System resource
# ============================
#cd('/')
#create('myJmsSystemResource', 'JMSSystemResource')
#cd('JMSSystemResource/myJmsSystemResource/JmsResource/NO_NAME_0')

# Create a JMS Queue and its subdeployment
# ========================================
#myq=create('myQueue','Queue')
#myq.setJNDIName('jms/myqueue')
#myq.setSubDeploymentName('myQueueSubDeployment')

#cd('/')
#cd('JMSSystemResource/myJmsSystemResource')
#create('myQueueSubDeployment', 'SubDeployment')

# Create and configure a JDBC Data Source, and sets the JDBC user
# ===============================================================
# IF YOU WANT TO HAVE A DEFAULT DATA SOURCE CREATED, UNCOMMENT THIS SECTION BEFORE BUILD

cd('/')
create('ATGPublishingDS', 'JDBCSystemResource')
cd('JDBCSystemResource/ATGPublishingDS/JdbcResource/ATGPublishingDS')
create('ATGPublishingDSParams','JDBCDriverParams')
cd('JDBCDriverParams/ATG_PUB')
set('DriverName','oracle.jdbc.xa.client.OracleXADataSource')
set('URL','jdbc:oracle:thin:@oracledb.cenfyitgwkcr.us-west-2.rds.amazonaws.com:1521:orcl')
set('PasswordEncrypted', 'ATG_PUB')
set('UseXADataSourceInterface', 'true')
create('myProps','Properties')
cd('Properties/ATG_PUB')
create('user', 'Property')
cd('Property/user')
cmo.setValue('ATG_PUB')

cd('/JDBCSystemResource/ATGPublishingDS/JdbcResource/ATGPublishingDS')
create('ATGPublishingDSParams','JDBCDataSourceParams')
cd('JDBCDataSourceParams/ATG_PUB')
set('JNDIName', java.lang.String("ATG_PUB"))

cd('/JDBCSystemResource/ATGPublishingDS/JdbcResource/ATGPublishingDS')
create('myJdbcConnectionPoolParams','JDBCConnectionPoolParams')
cd('JDBCConnectionPoolParams/ATG_PUB')
set('TestTableName','SYSTABLES')
set('MaxCapacity','50')

# Target resources to the servers 
# ===============================
cd('/')
#assign('JMSServer', 'myJMSServer', 'Target', 'AdminServer')
#assign('JMSSystemResource.SubDeployment', 'myJmsSystemResource.myQueueSubDeployment', 'Target', 'myJMSServer')
assign('JDBCSystemResource', 'ATGPublishingDS', 'Target', 'StoreFront')

# Write the domain and close the domain template
# ==============================================
setOption('OverwriteDomain', 'true')
setOption('ServerStartMode','dev')

cd('/')
cd('NMProperties')
set('ListenAddress','')
set('ListenPort',5556)
set('NativeVersionEnabled', 'false')
set('StartScriptEnabled', 'false')
set('SecureListener', 'false')

domain_path = '/u01/oracle/weblogic/user_projects/domains/base_domain'

writeDomain(domain_path)
closeTemplate()

# Enable JAX-RS 2.0 by default on this domain
# ===========================================
readDomain(domain_path)
addTemplate('/u01/oracle/jaxrs2-template.jar')
updateDomain()
closeDomain()

# Exit WLST
# =========
exit()

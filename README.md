-----------------------------------------------------------Data as a Service-----------------------------------------------------------
- Dependencies:
	- Hadoop Cluster for HDFS ()
	- Spark Cluster for Spark SQL processing
	- Web2py for appserver
- Installation:
	- After Hadoop cluster installation, Deploy FileServer.py on namenode and run as:
		python FileServer.py 5555
	- After Spark cluster installation, Deploy SparkServer.py on Spark master and run as:
		python SparkServer.py 5555
	- Deploy web2py.app.sparkapp.w2p to Spark master with Web2py running by importing as existing applications
		Run web2py on port 8000
	- Hosts running Spark master should be named as "harish" in /etc/hosts, whereas the namenode should be named "ahmedali" in /etc/hosts for both Spark master and HDFS namenode.
	- The app has been setup.

- App URL: http://harish:8000/sparkapp/default
- Monitoring:
	- HDFS namenode: http://ahmedali:50070/
	- Spark Cluster: http://harish:8080
	

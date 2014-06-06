import sys  
from hive_service import ThriftHive  
from hive_service.ttypes import HiveServerException  
from thrift import Thrift  
from thrift.transport import TSocket  
from thrift.transport import TTransport  
from thrift.protocol import TBinaryProtocol  
  
def hiveExe(sql):  
     
       try:  
           transport = TSocket.TSocket('127.0.0.1', 10000)   
	   transport = TTransport.TBufferedTransport(transport)  
           protocol = TBinaryProtocol.TBinaryProtocol(transport)  
           client = ThriftHive.Client(protocol)  
           transport.open()  
           client.execute(sql)  
           print "The return value is : "   
	   print client.fetchAll()  
           print "............"  
	   transport.close()  
       except Thrift.TException, tx:  
           print '%s' % (tx.message) 
if __name__ == '__main__':
           hiveExe("show tables")  

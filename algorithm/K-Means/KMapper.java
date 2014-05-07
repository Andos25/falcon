package example;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.net.URI;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;


public class KMapper extends Mapper<LongWritable, Text, Text, Text> {
    
	private Map[] centerMap = new Map[10];//k=10
    private String[] center;
    protected void setup(Context context) throws IOException,InterruptedException
    {
    	for(int i=0;i<centerMap.length;i++){
 		   centerMap[i] = new HashMap<String,String>();
 	   	}
    	String centerlist = "hdfs://192.168.40.161:9000/kmeansinput/clustercenter.txt";
        Configuration conf1 = new Configuration();
        conf1.set("hadoop.job.ugi", "hadoop-user,hadoop-user");
        FileSystem fs = FileSystem.get(URI.create(centerlist),conf1);
        FSDataInputStream in = null;
        ByteArrayOutputStream out = new ByteArrayOutputStream();
       try{
           in = fs.open( new Path(centerlist) );
           IOUtils.copyBytes(in,out,100,false);  
           center = out.toString().split("}");
           System.out.println("center.length="+center.length);
           for(int i=0;i<center.length;i++){
        	   String[] tmp;
        	   tmp = center[i].replace("{", "").split(",");
        	   System.out.println("center["+i+"]="+center[i]);
        	   for(int j=0;j<tmp.length;j++){
        		   centerMap[i].put(tmp[j].split(":")[0], tmp[j].split(":")[1]);
        		   }
           }
           }finally{
                IOUtils.closeStream(in);
            }
    }
    
    public void map(LongWritable key,Text value,Context context) throws IOException,InterruptedException
    {
    	System.out.println("start mapper!");
        StringTokenizer itr = new StringTokenizer(value.toString(),"\n");
        while(itr.hasMoreTokens())
        {
            String outValue = new String(itr.nextToken());
            outValue = outValue.replace(" ", "");
            System.out.println("outValue="+outValue);
            String blogId = outValue.split("\t")[0];
            String vector = outValue.split("\t")[1];
            System.out.println("blogId="+blogId);
            System.out.println("vector="+vector);
            String[] list = vector.replace("{", "").replace("}", "").split(",");
            Map v = new HashMap<String,String>();
            for(int i =0; i<list.length; i++){
            	v.put(list[i].split(":")[0], list[i].split(":")[1]);
            }
            float min = 0;
            int pos = 0;
            Set<Entry<String, String>> vsets = v.entrySet();  
            for(Entry<String, String> entry : vsets) { 
            	if(centerMap[0].containsKey(entry.getKey())){
            		min += Math.pow(Float.parseFloat(entry.getValue()) - Float.parseFloat((String) centerMap[0].get(entry.getKey())), 2);
            	}else{
            		min += Math.pow(Float.parseFloat(entry.getValue()), 2);
            	}
            }  
            Set<Entry<String, String>> csets = centerMap[0].entrySet();
            for(Entry<String, String> entry : csets) {
            	if(!(v.containsKey(entry.getKey()))){
            		min += Math.pow(Float.parseFloat(entry.getValue()), 2);
            	}
            }  
        	System.out.println("min="+ min);
        	
            for(int i=0;i<centerMap.length;i++){
                float distance = 0;
                for(Entry<String, String> entry : vsets) {
                	if(centerMap[i].containsKey(entry.getKey())){
                		distance += (float) Math.pow((Float.parseFloat(entry.getValue()) - Float.parseFloat((String) centerMap[i].get(entry.getKey()))),2);
                	}else{
                		distance += Math.pow(Float.parseFloat(entry.getValue()), 2);
                	}
                }  
                csets = centerMap[i].entrySet();
                for(Entry<String, String> entry : csets) {
                	if(!(v.containsKey(entry.getKey()))){
                		distance += Math.pow(Float.parseFloat(entry.getValue()), 2);
                	}
                }
                
                System.out.println("distance"+i+"="+distance);
                if(distance<min){
                	min = distance;
                	pos=i;
                }
            }
            System.out.println("clusterId="+pos);
            System.out.println("outValue.split({)[1]="+outValue.split("\\{")[1]);
            System.out.println("Mapper输出："+center[pos]+"}"+" "+outValue);
            outValue = blogId + "@{" + outValue.split("\\{")[1];
            System.out.println("中心点"+center[pos]+"}"+"对应坐标"+outValue);
            context.write(new Text(center[pos]+"}"), new Text(outValue));
            
        }
    }
}

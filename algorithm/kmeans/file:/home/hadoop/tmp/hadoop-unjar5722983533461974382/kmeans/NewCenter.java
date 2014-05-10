package kmeans;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.URI;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.Map.Entry;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;

public class NewCenter {
	float shold=Integer.MIN_VALUE;
	float[] res ={0, 0};
	String[] line;
	String newcenter = new String("");
	@SuppressWarnings({ "rawtypes", "unchecked" })
	public float[] run(String[] args) throws IOException,InterruptedException
	{
		Configuration conf = new Configuration();
		conf.set("hadoop.job.ugi", "hadoop,hadoop");
		String inpath = "hdfs://192.168.40.161:9000/kmeansoutput/part-r-00000";
		FileSystem fs = FileSystem.get(URI.create(inpath),conf);
		FSDataInputStream in = null;
		ByteArrayOutputStream out = new ByteArrayOutputStream();
		try{ 
			in = fs.open( new Path(inpath)); 
			IOUtils.copyBytes(in,out,50,false);
			line = out.toString().split("\n");
//			System.out.println("out:"+out);
			} finally { 
				IOUtils.closeStream(in);
			}
//		System.out.println("上一次的MapReduce结果："+out.toString());
//		System.out.println("line.length="+line.length);//=k
		for(int i=0;i<line.length;i++)
		{
			String[] l = line[i].replace("\t", "").split("}");
			String[] startCenter = l[0].replace("{", "").split(",");
//			System.out.println("oldcenter="+l[0]+"}");
			String[] finalCenter = l[l.length-1].split("\\{")[1].split(",");
//			System.out.println("newcenter="+"{"+l[l.length-1].split("\\{")[1]+"}");
			Map oldCen = new HashMap<String,String>();
			for(int o=0;o<startCenter.length;o++){
				oldCen.put(startCenter[o].split(":")[0], startCenter[o].split(":")[1]);
			}
			Map newCen = new HashMap<String,String>();
			for(int n=0;n<finalCenter.length;n++){
				newCen.put(finalCenter[n].split(":")[0], finalCenter[n].split(":")[1]);
			}
			float tmp = 0;
			Set<Entry<String, String>> osets = oldCen.entrySet();  
            for(Entry<String, String> entry : osets) {
            	if(newCen.containsKey(entry.getKey())){
            		tmp += Math.pow(Float.parseFloat(entry.getValue()) - Float.parseFloat((String)newCen.get(entry.getKey())), 2);
            	}else{
            		tmp += Math.pow(Float.parseFloat(entry.getValue()), 2);
            	}
            }  
            Set<Entry<String, String>> nsets = newCen.entrySet();
            for(Entry<String, String> entry : nsets) {
            	if(!(oldCen.containsKey(entry.getKey()))){
            		tmp += Math.pow(Float.parseFloat(entry.getValue()), 2);
            	}
            }  
			newcenter = newcenter + "{" + l[l.length - 1].split("\\{")[1] + "}";
			if(shold <= tmp)
				shold = tmp;
//			System.out.println(i+"差异："+tmp);
		}
//		System.out.println("新中心点："+newcenter);
		OutputStream out2 = fs.create(new Path("hdfs://192.168.40.161:9000/kmeansinput/clustercenter.txt"));
//		System.out.println("newcenter**************"+newcenter);
//		System.out.println("newCenter:::::::length::::::::"+newcenter.split("}").length);
		IOUtils.copyBytes(new ByteArrayInputStream(newcenter.getBytes()), out2, 4096,true);
		res[0] = shold;
		res[1] = newcenter.split("}").length; 
		return res;
	}
}

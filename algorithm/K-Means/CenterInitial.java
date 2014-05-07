package example;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.URI;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;


public class CenterInitial {
	
	
	public void run(String[] args) throws IOException
	{
		String[] clist;
		int k = 10;
		String string = "";
		String inpath = "hdfs://192.168.40.161:9000/kmeansinput/samplev.txt";
		String outpath = "hdfs://192.168.40.161:9000/kmeansinput/clustercenter.txt";
		Configuration conf1 = new Configuration();
		conf1.set("hadoop.job.ugi", "hadoop,hadoop");
		FileSystem fs = FileSystem.get(URI.create(inpath),conf1);
		FSDataInputStream in = null; 
		ByteArrayOutputStream out = new ByteArrayOutputStream();
		try{
			in = fs.open( new Path(inpath) ); 
			IOUtils.copyBytes(in,out,50,false);
			clist = out.toString().split("\n");
			} finally { 
				IOUtils.closeStream(in);
			}
		
		FileSystem filesystem = FileSystem.get(URI.create(outpath), conf1);
		for(int i=0;i<k;i++)
		{
			int j=(int) (Math.random()*100) % clist.length;
			if(string.indexOf(clist[j].split("\t")[1])!=-1)
			{
				k++;
				continue;
			}
			string = string + clist[j].replace(" ", "").split("\t")[1];
		}
		OutputStream out2 = filesystem.create(new Path(outpath) ); 
		IOUtils.copyBytes(new ByteArrayInputStream(string.getBytes()), out2, 4096,true);
		System.out.println("初始化过程："+string);
	}

}

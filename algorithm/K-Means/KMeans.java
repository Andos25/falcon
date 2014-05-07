package example;

import java.io.FileOutputStream;
import java.io.PrintStream;

import org.apache.hadoop.conf.Configuration;  
import org.apache.hadoop.fs.FileSystem;  
import org.apache.hadoop.fs.Path;  
import org.apache.hadoop.io.Text;  
import org.apache.hadoop.mapreduce.Job;  
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;  
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;  
  
public class KMeans {  
      
    public static void main(String[] args) throws Exception  
    {
    	//将console输出写入文件
    	FileOutputStream bos = new FileOutputStream("example_log.txt");  
    	System.setOut(new PrintStream(bos));
    	
        CenterInitial centerInitial = new CenterInitial();  
        centerInitial.run(args);
        int times=0;  
        double s = 0,shold = 0.01;  
//        do {  
            Configuration conf = new Configuration();  
            conf.set("fs.default.name", "hdfs://192.168.40.161:9000");  
            Job job = new Job(conf,"KMeans");
            job.setJarByClass(KMeans.class);
            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(Text.class);
            job.setMapperClass(KMapper.class);
            job.setMapOutputKeyClass(Text.class);  
            job.setMapOutputValueClass(Text.class);
            job.setReducerClass(KReducer.class);  
            FileSystem fs = FileSystem.get(conf);  
            fs.delete(new Path("hdfs://192.168.40.161:9000/kmeansoutput"),true);
            FileInputFormat.addInputPath(job, new Path("hdfs://192.168.40.161:9000/kmeansinput/samplev.txt"));  
            FileOutputFormat.setOutputPath(job, new Path("hdfs://192.168.40.161:9000/kmeansoutput"));
            job.waitForCompletion(true);
            System.out.println("wait for complete");
            if(job.waitForCompletion(true))
            {  
                NewCenter newCenter = new NewCenter();  
                s = newCenter.run(args);  
                System.out.println("s="+s);
                times++;  
            }  
//        } while(s > shold);
        System.out.println("Iterator: " + times);
    }  
  
}

package KMeans;

import java.io.FileOutputStream;
import java.io.PrintStream;

import org.apache.hadoop.conf.Configuration;  
import org.apache.hadoop.fs.FileSystem;  
import org.apache.hadoop.fs.Path;  
import org.apache.hadoop.io.Text;  
import org.apache.hadoop.mapreduce.Job;  
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;  
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;  

import KMeans.CenterInitial;
import KMeans.KMapper;
import KMeans.KReducer;
import KMeans.NewCenter;
  
public class KMeans {  
      
    public static void main(String[] args) throws Exception  
    {  
//    	//将console输出写入文件
//        FileOutputStream bos = new FileOutputStream("log.txt");  
//        System.setOut(new PrintStream(bos));
        
        CenterInitial centerInitial = new CenterInitial();  
        centerInitial.run(args);//初始化中心点  
        int times=0;  
        double s = 0,shold = 0.01;//shold是预制。  
        do { 
        	
            Configuration conf = new Configuration();  
            conf.set("fs.default.name", "hdfs://192.168.40.161:9000");  
            Job job = new Job(conf,"KMeans");//建立KMeans的MapReduce作业  
            job.setJarByClass(KMeans.class);//设定作业的启动类  
            job.setOutputKeyClass(Text.class);//设定Key输出的格式：Text  
            job.setOutputValueClass(Text.class);//设定value输出的格式：Text  
            job.setMapperClass(KMapper.class);//设定Mapper类  
            job.setMapOutputKeyClass(Text.class);  
            job.setMapOutputValueClass(Text.class);//设定Reducer类  
            job.setReducerClass(KReducer.class);  
            FileSystem fs = FileSystem.get(conf);  
            fs.delete(new Path("hdfs://192.168.40.161:9000/kmeansoutput"),true);//args[2]是output目录，fs.delete是将已存在的output删除  
            //解析输入和输出参数，分别作为作业的输入和输出，都是文件   
            FileInputFormat.addInputPath(job, new Path("hdfs://192.168.40.161:9000/vectorize/part-00000"));  
            FileOutputFormat.setOutputPath(job, new Path("hdfs://192.168.40.161:9000/kmeansoutput"));  
            //运行作业并判断是否完成成功  
            System.out.println("waitForCompletion1");
            job.waitForCompletion(true); 
            System.out.println("waitForCompletion2");
            if(job.waitForCompletion(true))//上一次mapreduce过程结束  
            {  
            	System.out.println("job Complete!!!");
            	//上两个中心点做比较，如果中心点之间的距离小于阈值就停止；如果距离大于阈值，就把最近的中心点作为新中心点  
                NewCenter newCenter = new NewCenter();  
                s = newCenter.run(args);  
                System.out.println("s="+s);
                times++;  
            } 
        } while(s > shold);//当误差小于阈值停止。  
        System.out.println("Iterator: " + times);//迭代次数       
    }
/*        CenterInitial centerInitial = new CenterInitial();  
        centerInitial.run(args);//初始化中心点  
        int times=0;  
        double s = 0,shold = 0.01;//shold是阈值  
        
        do {//当误差小于阈值停止。 
        	System.out.println("Configuration");
            Configuration conf = new Configuration();  
            conf.set("fs.default.name", "hdfs://192.168.40.161:9000");
            System.out.println("job=KMeans");
            Job job = new Job(conf,"KMeans");//建立KMeans的MapReduce作业  
            job.setJarByClass(KMeans.class);//设定作业的启动类  
            job.setOutputKeyClass(Text.class);//设定Key输出的格式：Text  
            job.setOutputValueClass(Text.class);//设定value输出的格式：Text 
            
            System.out.println("setMapperClass");
            job.setMapperClass(KMapper.class);//设定Mapper类  
            job.setMapOutputKeyClass(Text.class);  
            job.setMapOutputValueClass(Text.class);  
            
            System.out.println("setReducerClass");
            job.setReducerClass(KReducer.class);//设定Reducer类  
            FileSystem fs = FileSystem.get(conf);  
            fs.delete(new Path("hdfs://192.168.40.161:9000/kmeansoutput"),true);//args[2]是output目录，fs.delete是将已存在的output删除  
            //解析输入和输出参数，分别作为作业的输入和输出，都是文件   
            FileInputFormat.addInputPath(job, new Path("hdfs://192.168.40.161:9000/vectorize/part-00000"));  
            FileOutputFormat.setOutputPath(job, new Path("hdfs://192.168.40.161:9000/kmeansoutput"));  
            //运行作业并判断是否完成成功
            System.out.println("waitForCompletion");
            job.waitForCompletion(true);  
            if(job.waitForCompletion(true))//上一次mapreduce过程结束  
            {  
            	System.out.println("job Complete!!!");
                //上两个中心点做比较，如果中心点之间的距离小于阈值就停止；如果距离大于阈值，就把最近的中心点作为新中心点  
            	NewCenter newCenter = new NewCenter();  
                s = newCenter.run(args);  
                System.out.println("s="+s);
                times++;  
                System.out.println("Iterator: " + times);//迭代次数  
            }   
        }while(s>shold);
 */    }    
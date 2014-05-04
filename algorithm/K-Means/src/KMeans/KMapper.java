package KMeans;

import java.io.ByteArrayOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.net.URI;
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
    
    private String[] center;
    //读取clustercenter.txt中更新的中心点坐标，并将坐标存入center数组中
    protected void setup(Context context) throws IOException,InterruptedException  //read centerlist, and save to center[]
    {
        String centerlist = "hdfs://192.168.40.161:9000/kmeansinput/clustercenter.txt"; //center文件
        Configuration conf1 = new Configuration();
        conf1.set("hadoop.job.ugi", "hadoop-user,hadoop-user");
       FileSystem fs = FileSystem.get(URI.create(centerlist),conf1);
       FSDataInputStream in = null;
       ByteArrayOutputStream out = new ByteArrayOutputStream();
       try{
           in = fs.open( new Path(centerlist) );
           IOUtils.copyBytes(in,out,100,false);  
           center = out.toString().split("] ");
           }finally{
                IOUtils.closeStream(in);
            }
//       System.out.println("mapper setup");
    }
    //从hadoop接收的数据在2.txt中保存
    public void map(LongWritable key,Text value,Context context) throws IOException,InterruptedException
    {
//    	System.out.println("start mapper!");
        StringTokenizer itr = new StringTokenizer(value.toString(), "\n");
        //针对每一行：74161 [0, 0, 0,...,0]
        while(itr.hasMoreTokens())//用于判断所要分析的字符串中，是否还有语言符号，如果有则返回true，反之返回false
        {
            //计算第一个坐标跟第一个中心的距离min
            String outValue = new String(itr.nextToken());//逐个获取以空格为分割符的字符串(2,3) (10,30) (34,40) (1,1)
//            System.out.println("outValue="+outValue);//输出每一行长什么样子
            String blogId = outValue.split(" \\[")[0];
            outValue = outValue.split(" \\[")[1];
            String[] list = outValue.replace("]", "").split(", ");//list=[2,3]
//            System.out.println("running!");
            
            float min = 0;
            int pos = 0;
            String[] c = center[0].replace("[", "").split(", ");//center[i]存放第i个clustercenter向量
//            System.out.println("center[0]="+center[0]);
            for(int i=0;i<list.length;i++)//list存放该微博vector
            {
//                System.out.println(i+"list:"+list[i]);
//                System.out.println(i+"c:"+c[i]);
                min += (float) Math.pow((Float.parseFloat(list[i]) - Float.parseFloat(c[i])),2);//求欧氏距离，未加根号
            }
            System.out.println("min="+min);
            //center[i]:[0, 0, 0,...,0]
            for(int i=0;i<center.length;i++)
            {
                String[] centerStrings = center[i].replace("[", "").split(", ");
                float distance = 0;
                for(int j=0;j<list.length;j++)
                    distance += (float) Math.pow((Float.parseFloat(list[j]) - Float.parseFloat(centerStrings[j])),2);
                System.out.println("distance["+i+"]:"+distance);
                if(min>distance)
                {
                    min=distance;
                    pos=i;
                }
            }
            context.write(new Text(center[pos]+"]"), new Text(blogId+"@"+"["+outValue));//输出：中心点，对应的坐标
//            System.out.println("中心点"+center[pos]+"]"+"对应坐标"+blogId+"@"+"["+outValue);
            System.out.println("Mapper输出："+center[pos]+"]"+" "+blogId+"@"+"["+outValue); 
        }
    }
}
package KMeans;

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
  
  
public class NewCenter {  
      
    int k = 3;  
    float shold=Integer.MIN_VALUE;  
    String[] line;  
    String newcenter = new String("");  
      
    public float run(String[] args) throws IOException,InterruptedException  
    {  
        Configuration conf = new Configuration();  
        conf.set("hadoop.job.ugi", "hadoop,hadoop");
        //<old center> <new center>存放在/kmeansoutput/part-r-00000；old center存放在/kmeansinput/clustercenter.txt；每次mapreduce结束即更新clustercenter.txt
        FileSystem fs = FileSystem.get(URI.create("hdfs://192.168.40.161:9000/kmeansoutput/part-r-00000"),conf);  
        FSDataInputStream in = null;  
        ByteArrayOutputStream out = new ByteArrayOutputStream();  
        try{   
            in = fs.open( new Path("hdfs://192.168.40.161:9000/kmeansoutput/part-r-00000"));   
            IOUtils.copyBytes(in,out,50,false);  
            line = out.toString().split("\n");  //每一行：[old center] [new center]
            } finally {   
                IOUtils.closeStream(in);  
            }  
      
        //System.out.println("上一次的MapReduce结果："+out.toString());  
//        System.out.println("上一次MapReduce结果：cluster0："+line[0]);  
//        System.out.println("cluster1："+line[1]);  
        //计算k对新旧中心的欧氏距离，选取最大的距离为新旧差距，最后返回并与阈值比较
        for(int i=0;i<k;i++) //k为多少，就有多少行，即多少对<old center> <new center> 
        {  //针对每一行，即每一对<old center> <new center>，
            String[] l = line[i].split("]");//如果这行有tab的空格，可以替代为空格  
            //(key,values)key和values同时输出是，中间保留一个Tab的距离，即'\t'  
            String[] oldCenter = l[0].replace("[", "").split(", ");  
            //上上次的中心点oldCenter[0]=(10,30);oldCenter[1]=(2,3);  
            String[] newCenter = l[l.length-1].replace("[", "").split(", ");  
            //上一次的中心点newCenter[0]=(22,35);newCenter[1]=(1.5,2.0);  
            float tmp = 0;  
            for(int j=0;j<oldCenter.length;j++)  
                tmp += Math.pow(Float.parseFloat(oldCenter[j])-Float.parseFloat(newCenter[j]), 2);  
            //两个中心点间的欧式距离
            newcenter = newcenter + l[l.length - 1] + "]";  
            if(shold <= tmp)  
                shold = tmp;//shold取k对新旧中心点之间最大的平方差的和
//            System.out.println(i+"坐标距离："+tmp);  
        }  
        OutputStream out2 = fs.create(new Path("hdfs://192.168.40.161:9000/kmeansinput/clustercenter.txt") );   
        IOUtils.copyBytes(new ByteArrayInputStream(newcenter.getBytes()), out2, 4096,true);  
//        System.out.println("newcenter:"+newcenter);  
        return shold;  
    }  
  
}

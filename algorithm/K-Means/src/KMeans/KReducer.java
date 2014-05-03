package KMeans;

import java.io.FileOutputStream;
import java.io.IOException;  
import java.io.PrintStream;

import org.apache.hadoop.io.Text;  
import org.apache.hadoop.mapreduce.Reducer;  

public class KReducer extends Reducer<Text, Text, Text, Text> {  
    //<中心点类别,中心点对应的坐标集合>,每个中心点类别的坐标集合求新的中心点  
      
    public void reduce(Text key,Iterable<Text> value,Context context) throws IOException,InterruptedException  
    {   
        String outVal = "";  
        int count=0;  
        String center="";  
        System.out.println("start reduce!!!");  
//        System.out.println("mapper key="+key.toString());  
        //clustercenter's length
        int length = key.toString().replace("\\[", "").replace("\\]", "").split(", ").length;  
        float[] ave = new float[Float.SIZE*length];  
//        System.out.println("length="+length);
        for(int i=0;i<length;i++)  
            ave[i]=0;   
        for(Text val:value)  //针对同一key中的各个value
        {   //mapper value:79023@[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ... ,0]
//            System.out.println("mapper value:"+val.toString());
            //values:org.apache.hadoop.mapreduce.task.ReduceContextImpl$ValueIterable@4f9faf3
//            System.out.println("values:"+value.toString());  
            outVal += val.toString()+" ";  
            //tmp[]:存储一条vector的信息
            String[] tmp = val.toString().split("@")[1].replace("[", "").replace("]", "").split(", ");  
//            System.out.println("temlength:"+tmp.length);  
            for(int i=0;i<tmp.length;i++)  
                ave[i] += Float.parseFloat(tmp[i]);
            count ++;  //count存储属于该cluster的vector总数
        }  
//        System.out.println("count:"+count);  
//        System.out.println("outVal:"+outVal+"/outVal");  
//        for (int i=0;i<length;i++)  
//        {  
//            System.out.println("ave"+i+"i"+ave[i]);  
//        }  
        //ave[i]存储所有vector第ith坐标之和 
        for(int i=0;i<length;i++)  
        {  
            ave[i]=ave[i]/count;  
            if(i==0)  
                center += "["+ave[i]+", ";  
            else {  
                if(i==length-1)  
                    center += ave[i]+"]";  
                else {  
                    center += ave[i]+", ";  
                }  
            }  
        }  

        System.out.println("写入part："+key+ " "+center); //key:old center; center: new center 
        context.write(key, new Text(center));  
    }  
  
}

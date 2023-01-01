
function reset()
   {
      var exnum=[]
      i=0
      for (j=1;j<26;j++)
        {btid="btn"+j
        
            document.getElementById(btid).innerHTML='&nbsp;';

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
     

    }
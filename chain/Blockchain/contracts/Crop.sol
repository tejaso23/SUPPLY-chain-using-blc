// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

// Manufcturer 
// distributor
// retilor

contract Crop {   
    
    mapping(uint256 => proddetails) prodlist;   
     
     struct proddetails{
     uint256 prod_id;
     string cropname;
     string fname;
     string faddress;
     string prodname;
     uint256 prodprice;   
     string manudate;
     string processnames;     
     
     }
     proddetails prod;
    


     mapping(uint256 => distributordetails) distributorlist;
     struct distributordetails{
        uint256 prod_id;
        string distributorname;
        uint256 dkycid;
        string daddress;
        uint256 dcontact;
     } distributordetails distributor;



     mapping(uint256 => retailerdetails) retailerlist;
     struct retailerdetails{
        uint256 prod_id;
        string retailername;
        uint256 rkycid;
        string raddress;
        uint256 rcontact;
     } retailerdetails retailer;



 function store_prod_details(uint256 _prod_id,string memory _cropname, string memory _fname, string memory _faddress, string memory _prodname, uint256 _prodprice,string memory _manudate, string memory _processnames)public {
     
         prod.prod_id=_prod_id;
         prod.cropname=_cropname;
         prod.fname=_fname;
         prod.faddress=_faddress;
         prod.prodname=_prodname;         
         prod.prodprice=_prodprice;
         prod.manudate=_manudate;
         prod.processnames=_processnames;      
         prodlist[_prod_id] = prod;
         }




 function store_distributor_details(uint256 _prod_id, string memory _distributorname, uint256 _dkycid, string memory _daddress, uint256 _dcontact)public {
     
         distributor.prod_id=_prod_id;
         distributor.distributorname=_distributorname;
         distributor.dkycid=_dkycid;
         distributor.daddress=_daddress;         
         distributor.dcontact=_dcontact;
         distributorlist[_prod_id] = distributor;
         }


 function store_retailer_details(uint256 _prod_id, string memory _retailername, uint256 _rkycid, string memory _raddress, uint256 _rcontact)public {
     
         retailer.prod_id=_prod_id;
         retailer.retailername=_retailername;
         retailer.rkycid=_rkycid;
         retailer.raddress=_raddress;       
         retailer.rcontact=_rcontact;
         retailerlist[_prod_id] = retailer;
         }






     function retreive_prod_details(uint256 prod_id) public view returns (uint256, string memory, string memory, string memory, string memory, uint256, string memory, string memory){
         proddetails memory prod = prodlist[prod_id];
         
       return (prod_id,prod.cropname,prod.fname,prod.faddress,prod.prodname,prod.prodprice,prod.manudate, prod.processnames);
    
     }




     function retreive_distributor_details(uint256 prod_id) public view returns (uint256, string memory, uint256, string memory, uint256){
         distributordetails memory distributor = distributorlist[prod_id];
         
       return (prod_id,distributor.distributorname,distributor.dkycid,distributor.daddress,distributor.dcontact);
    
     }


     function retreive_retailer_details(uint256 prod_id) public view returns (uint256, string memory, uint256, string memory, uint256){
         retailerdetails memory retailer = retailerlist[prod_id];
         
       return (prod_id,retailer.retailername,retailer.rkycid,retailer.raddress,retailer.rcontact);
    
     }


}
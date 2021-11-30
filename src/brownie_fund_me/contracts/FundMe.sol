// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;
//pragma solidity >=0.6.6 <0.9.0;
//pragma solidity >=0.8.1 <0.9.0;

//import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
//import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    
    mapping(address => uint256) public addressToAmountFunded;
//    AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e); //Rinkeby
    AggregatorV3Interface public priceFeed;
    address public owner = msg.sender;
    address[] public funders;

     constructor(address _priceFeed) public{
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed);
     }

 
    function fund() public payable {
        // $50
        // uint256 minimumUSD = 50 * 10 ** 18;
        
        // require(getConversionRate(msg.value) >= minimumUSD, "You need to spend more ETH!");

        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);

    }   

    function getVersion() public view returns(uint256){
        // AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e); //Rinkeby
        return priceFeed.version();
    }
    
    function getPrice() public view returns(uint256){
        ( , int price,,,) = priceFeed.latestRoundData();
        return uint256(price * 10000000000);
    }
    
    //1000000000 wei = 1gwei = 0.000000001eth  https://eth-converter.com/
    function getConversionRate(uint256 ethAmount) public view returns(uint256){ 
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000 ;
        // 4764978895400.000000000000000000
        return ethAmountInUsd; //returns in gwei !!
    }

     function getEntranceFee() public view returns (uint256) {
        // mimimumUSD
        uint256 mimimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (mimimumUSD * precision) / price;
    }

    modifier onlyOwner {
        // only want the contract admin/owner
        require( msg.sender == owner, "The Sender needs to be the owner!" );
        _;
        
    }
    
    function withdraw() payable onlyOwner public { //https://ethereum.stackexchange.com/questions/102346/transfer-only-available-for-objects-of-type-address-payable-not-address
        payable(msg.sender).transfer(address(this).balance); //transfer to the caller all of our money
        for (uint256 funderIndex=0; funderIndex < funders.length; funderIndex++){
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
            
        }
        
        funders = new address[](0);
        
    }//withdraw()
    
    
    
}//FundMe

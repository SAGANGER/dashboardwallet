import json

# Liste originale
wallets = [
    
  {
    "wallet_address": "5qW7o1zkd2fS9yuck2MPYe6uPYahh18UwDBpK9cukJaK"
  },
  {
    "wallet_address": "FADdUH84jL8coWyCJjqpdHVBqut1hRGUn55EVcCZZJkw"
  },
  {
    "wallet_address": "9y9G5oPHigVCZbNbE83EemkpV1odxX2m99kU7AZCZ2Gp"
  },
  {
    "wallet_address": "3GEt212GAiHeG5ZAAX4JePbbhkFQjqFs4pC4E44LqKFg"
  },
  {
    "wallet_address": "CXW5rJE7PcHCUHNPskfVhFts1sxpzuedq94fL77gpVM3"
  },
  {
    "wallet_address": "8pM1DN3RiT8vbom5u1sNryaNT1nyL8CTTW3b5PwWXRBH"
  },
  {
    "wallet_address": "wallet_027"
  },
  {
    "wallet_address": "wallet_004"
  },
  {
    "wallet_address": "wallet_032"
  },
  {
    "wallet_address": "54kPLwyAF7MUjn8g1Ec2QAJQNLaTnw6ztuURTjCsUWSq"
  },
  {
    "wallet_address": "wallet_029"
  },
  {
    "wallet_address": "6XZg8QvhwwSvjsNfqscor67R1gcFDmJCsCRdyQZTmZH3"
  },
  {
    "wallet_address": "CZSCUnxH81JpLSB6pbW7u52Ww5ZDsHVNdKcRpM9vVP2v"
  },
  {
    "wallet_address": "wallet_005"
  },
  {
    "wallet_address": "wallet_011"
  },
  {
    "wallet_address": "9r3SQNWoHQPmYCdrgt3qBEHs6YPWGbTKE1SfRZYEuieF"
  },
  {
    "wallet_address": "7bVfeqJMRXNCK6p7tpx6xP9SuusuuV9NXdjrDAHPyx7p"
  },
  {
    "wallet_address": "9JRiJCr8HYSJYxj4r72wu6ZYYi4hzeCRVcUKhhpmVFp7"
  },
  {
    "wallet_address": "wallet_017"
  },
  {
    "wallet_address": "DraMAyJ6RPiTWHyB9g4UQmqfrPEEPDK4FffpvBo3zYSk"
  },
  {
    "wallet_address": "HMci7zs8rzpsKTe6157B2ar7gQXHpZe3sE19MvEkFZ8R"
  },
  {
    "wallet_address": "wallet_002"
  },
  {
    "wallet_address": "HTyHBqRskgU3pDZUQcHAEH5FR2eKtsJX6vjSKQUi8LXo"
  },
  {
    "wallet_address": "BMD9gkzegag9QLmzre8NNSBWWSsbzimwmKWdD4mbsiP6"
  },
  {
    "wallet_address": "wallet_039"
  },
  {
    "wallet_address": "H7LBEkkHZAsA3RzSkt5d8gbmBDDydmthAVqt6iZy8jFp"
  },
  {
    "wallet_address": "GoGrEGMXoZSvJLBj82gicHHHnFiemhSU2TcqBWvVicbV"
  },
  {
    "wallet_address": "wallet_040"
  },
  {
    "wallet_address": "wallet_021"
  },
  {
    "wallet_address": "AA5TeBo1dK4VLB1GEpY4a2vCfNgZAVjL5o6GBGiv4zSS"
  },
  {
    "wallet_address": "HC25BEDP1Be69EeL9WoZDBW9YpUNeKsw74k3yzSQE6es"
  },
  {
    "wallet_address": "AEV4WPU5DyWrJJ17ZfhqvYWr6G1FnvCKQvGsGeFh2anK"
  },
  {
    "wallet_address": "5KTPsBdeDuvZR1h7WjLHTpcApNyxLMiEFwUq6iwntKnr"
  },
  {
    "wallet_address": "5MuPeGnq9Ax1QJHfQukFfEJxHeU1PhtxSVDRb1GQpmBj"
  },
  {
    "wallet_address": "wallet_023"
  },
  {
    "wallet_address": "5fddi9FGztJ7cXcL9UzdUvidHKTx1ro9jRdQcV8B6zr7"
  },
  {
    "wallet_address": "86z7HXoUm5CwT4k696YTTJT11guCdpKNyxyBnhpmPHBV"
  },
  {
    "wallet_address": "wallet_036"
  },
  {
    "wallet_address": "wallet_020"
  },
  {
    "wallet_address": "wallet_003"
  },
  {
    "wallet_address": "wallet_012"
  },
  {
    "wallet_address": "4eJBkxwGY72oF2MNSVuPaG43miVzJ5UHeYh7AEexHyU3"
  },
  {
    "wallet_address": "wallet_031"
  },
  {
    "wallet_address": "wallet_008"
  },
  {
    "wallet_address": "i4FiJpw2xzmm2o4K5cqaKKCn81vXoM5v2vp11GnLyCZ"
  },
  {
    "wallet_address": "wallet_038"
  },
  {
    "wallet_address": "6Br9PGwAYrKYUha6RmTNkCNXfBdb9SRTY2GKq6mq3MjF"
  },
  {
    "wallet_address": "4eMDHRofQ1Mv853urQwqC6ZUrdXvj7p9iTNkGk7dVzDK"
  },
  {
    "wallet_address": "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU"
  },
  {
    "wallet_address": "wallet_009"
  },
  {
    "wallet_address": "wallet_015"
  },
  {
    "wallet_address": "wallet_010"
  },
  {
    "wallet_address": "wallet_025"
  },
  {
    "wallet_address": "DrLRPeEBZKEfSYyC9oHchvQzLRJCZ41fVQGbFyuzHDxL"
  },
  {
    "wallet_address": "5METitenYgUWqoKFDD7SXpMYrdUSAqT5juRU456D5Zjv"
  },
  {
    "wallet_address": "VGwt9nZvvRuCJz8PubthCAYoo3B9DSBrzTYARohCddo"
  },
  {
    "wallet_address": "wallet_033"
  },
  {
    "wallet_address": "wallet_001"
  },
  {
    "wallet_address": "8S7wmcFGNHsy9JbSLpjcN6XmqgsrjUgSvdmfZispbiz8"
  },
  {
    "wallet_address": "9VJXHY35QoeLU97WapqiPu2eKTN9HSJqCuARYZQJRQt"
  },
  {
    "wallet_address": "8RARWLw3ugG9ZadDeRxiXjPocQqG1d5UExjYifydXKFN"
  },
  {
    "wallet_address": "wallet_028"
  },
  {
    "wallet_address": "wallet_007"
  },
  {
    "wallet_address": "wallet_034"
  },
  {
    "wallet_address": "FXiHnY7VCrPoZKvWBYJdRUUF8v3F98ijkBybC3Eroh1L"
  },
  {
    "wallet_address": "wallet_006"
  },
  {
    "wallet_address": "wallet_030"
  },
  {
    "wallet_address": "wallet_022"
  },
  {
    "wallet_address": "wallet_130"
  },
  {
    "wallet_address": "wallet_018"
  },
  {
    "wallet_address": "66izVq4SWvANGDcFbsymxjAKLndLhU3aWD5MKLJBJ7Gn"
  },
  {
    "wallet_address": "wallet_019"
  },
  {
    "wallet_address": "wallet_024"
  },
  {
    "wallet_address": "wallet_037"
  },
  {
    "wallet_address": "wallet_026"
  },
  {
    "wallet_address": "wallet_016"
  },
  {
    "wallet_address": "wallet_013"
  },
  {
    "wallet_address": "wallet_014"
  },
  {
    "wallet_address": "5eJZZLUKhSAzVXsCiyq61m5LpovVxmE2oYuNZdjtazgZ"
  },
  {
    "wallet_address": "wallet_035"
  }

]

# Transformation en liste contenant uniquement les valeurs
transformed_wallets = [wallet["wallet_address"] for wallet in wallets]

# Affichage du résultat
print(transformed_wallets)

# Conversion en JSON formaté
json_output = json.dumps(transformed_wallets, indent=4)
print(json_output)

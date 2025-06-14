import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

interface WalletData {
  address: string;
  balance: number;
  usd_value: number | null;
  total_staked: number;
  staked_usd_value: number | null;
  transaction_count: number;
  token_count: number;
  last_transaction: any;
  tokens: any[];
  stake_accounts: any[];
  error?: string;
}

function App() {
  const [wallets, setWallets] = useState<string>('');
  const [leaderboard, setLeaderboard] = useState<WalletData[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedWallet, setSelectedWallet] = useState<WalletData | null>(null);

  const analyzeWallets = async () => {
    try {
      setLoading(true);
      setError(null);
      const walletList = JSON.parse(wallets);
      console.log('Sending request to backend with wallets:', walletList);
      const response = await axios.post('https://dashboardwallet.onrender.com/analyze', { wallets: walletList });
      console.log('Received response from backend:', response.data);
      setLeaderboard(response.data);
    } catch (error: any) {
      console.error('Error analyzing wallets:', error);
      setError(error.message || 'An error occurred while analyzing wallets');
      if (error.response) {
        console.error('Error response:', error.response.data);
        setError(`Error: ${error.response.data.detail || error.message}`);
      } else if (error.request) {
        console.error('No response received:', error.request);
        setError('No response received from server. Is the backend running?');
      }
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString();
  };

  // New function to format numbers
  const formatNumber = (num: number | null, decimals: number = 4) => {
    if (num === null || isNaN(num)) return 'N/A';
    return num.toLocaleString('en-US', { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black p-8">
      <div className="container mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
          Solana Wallet Dashboard
        </h1>
        
        <div className="grid grid-cols-10 gap-8">
          {/* Left side - Input */}
          <div className="col-span-3 bg-gray-800/50 backdrop-blur-sm p-6 rounded-xl shadow-xl border border-gray-700">
            <h2 className="text-2xl font-semibold mb-4 text-blue-400">Wallet Analysis</h2>
            <textarea
              className="w-full h-96 bg-gray-900/50 text-white p-4 rounded-lg mb-4 border border-gray-700 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all duration-200 custom-scrollbar"
              placeholder="Paste wallet addresses in JSON format..."
              value={wallets}
              style={{
                outline: 'none'}}
              onChange={(e) => setWallets(e.target.value)}
            />
            <button
              onClick={analyzeWallets}
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-500 hover:to-blue-600 text-white font-bold py-3 px-4 rounded-lg transition-all duration-200 transform hover:scale-[1.02] disabled:opacity-50 disabled:transform-none"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Analyzing...
                </span>
              ) : 'Analyze'}
            </button>
            {error && (
              <div className="mt-4 p-4 bg-red-900/50 text-white rounded-lg border border-red-800 animate-fade-in">
                {error}
              </div>
            )}
          </div>

          {/* Right side - Leaderboard */}
          <div className="col-span-7 bg-gray-800/50 backdrop-blur-sm p-6 rounded-xl shadow-xl border border-gray-700">
          <h2 className="text-2xl font-semibold mb-4 text-blue-400">
              Wallet Leaderboard | {leaderboard.length} Wallets | {formatNumber(leaderboard.reduce((sum, wallet) => sum + wallet.balance, 0))} SOL
              <span className="text-lg text-gray-300 ml-2">
                ${formatNumber(leaderboard.reduce((sum, wallet) => sum + (wallet.usd_value || 0), 0), 2)}
              </span>
            </h2>
            <div className="space-y-4 custom-scrollbar">
              {leaderboard.map((wallet, index) => (
                <div 
                  key={wallet.address} 
                  className="bg-gray-900/50 p-4 rounded-lg cursor-pointer hover:bg-gray-800/70 transition-all duration-200 transform hover:scale-[1.01] border border-gray-700 hover:border-blue-500/50"
                  onClick={() => setSelectedWallet(wallet)}
                >
                   <div className="flex justify-between items-center">
                    <div>
                      <span className="text-gray-400">#{index + 1}</span>
                      <span className="ml-2 font-mono text-blue-300">{wallet.address.slice(0, 8)}...{wallet.address.slice(-8)}</span>
                      <span className="ml-2 text-sm text-gray-400">
                        ({((wallet.balance / leaderboard.reduce((sum, w) => sum + w.balance, 0)) * 100).toFixed(2)}% of total)
                      </span>
                    </div>
                    <div className="text-right">
                      <div className="font-bold text-lg text-white">
                        {formatNumber(wallet.balance)} SOL
                      </div>
                      {wallet.usd_value !== null && (
                        <div className="text-sm text-gray-300">
                          ${formatNumber(wallet.usd_value, 2)}
                        </div>
                      )}
                      {wallet.total_staked > 0 && (
                        <div className="text-sm text-green-400 mt-1">
                          Staked: {formatNumber(wallet.total_staked)} SOL
                          {wallet.staked_usd_value !== null && (
                            <span className="text-gray-300 ml-2">
                              (${formatNumber(wallet.staked_usd_value, 2)})
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="mt-2 text-sm text-gray-300 grid grid-cols-3 gap-2">
                    
                    
                    
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Wallet Details Modal */}
        {selectedWallet && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in">
            <div className="bg-gray-800/90 p-6 rounded-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto shadow-2xl border border-gray-700">
              <div className="flex justify-between items-start mb-6">
                <h3 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
                  Wallet Details
                </h3>
                <button 
                  onClick={() => setSelectedWallet(null)}
                  className="text-gray-400 hover:text-white transition-colors duration-200"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </div>
              
              <div className="space-y-6">
                <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-700">
                  <h4 className="font-semibold mb-2 text-blue-400">Address</h4>
                  <a 
                    href={`https://solscan.io/account/${selectedWallet.address}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-mono break-all text-blue-300 hover:text-blue-200 underline transition-colors duration-200"
                  >
                    {selectedWallet.address}
                  </a>
                </div>

                <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-700">
                  <h4 className="font-semibold mb-2 text-blue-400">Balance</h4>
                  <p className="text-2xl font-bold text-white">{formatNumber(selectedWallet.balance)} SOL</p>
                  {selectedWallet.usd_value !== null && (
                    <p className="text-gray-300">${formatNumber(selectedWallet.usd_value, 2)}</p>
                  )}
                </div>

                {selectedWallet.total_staked > 0 && (
                  <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-700">
                    <h4 className="font-semibold mb-2 text-blue-400">Staking</h4>
                    <p className="text-2xl font-bold text-green-400">{formatNumber(selectedWallet.total_staked)} SOL staked</p>
                    {selectedWallet.staked_usd_value !== null && (
                      <p className="text-gray-300">${formatNumber(selectedWallet.staked_usd_value, 2)}</p>
                    )}
                  </div>
                )}

                <div className="grid grid-cols-2 gap-4">
                  
                  
                </div>

                {selectedWallet.last_transaction && (
                  <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-700">
                    <h4 className="font-semibold mb-2 text-blue-400">Last Transaction</h4>
                    <p className="font-mono break-all text-gray-300">{selectedWallet.last_transaction.signature}</p>
                    <p className="text-gray-300 mt-1">
                      {formatDate(selectedWallet.last_transaction.blockTime)}
                    </p>
                  </div>
                )}

                {selectedWallet.tokens.length > 0 && (
                  <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-700">
                    <h4 className="font-semibold mb-2 text-blue-400">Tokens Overview</h4>
                    <div className="space-y-2 max-h-48 overflow-y-auto pr-2">
                      {selectedWallet.tokens.map((token, index) => (
                        <div key={index} className="bg-gray-800/50 p-3 rounded border border-gray-700 hover:border-blue-500/50 transition-colors duration-200">
                          <p className="font-mono break-all text-gray-300 text-sm">{token.pubkey}</p>
                          {token.account?.data?.parsed?.info && (
                            <p className="text-gray-300 mt-1 text-sm">
                              Amount: {formatNumber(token.account.data.parsed.info.tokenAmount.uiAmount, token.account.data.parsed.info.tokenAmount.decimals)}
                              {token.account.data.parsed.info.mint && (
                                <span className="ml-2 text-gray-500">({token.account.data.parsed.info.mint.slice(0,4)}...)</span>
                              )}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

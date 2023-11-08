export interface ICryptoPrice {
  id: number;
  cryptocurrency: string;
  value: number;
}

export interface IPricesProps {
  cryptoPrices: ICryptoPrice[];
  onCryptoDataChange: (data: ICryptoPrice[]) => void;
}


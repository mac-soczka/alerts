import { ICryptoPrice } from "./Price";

export interface IAlert {
  id: number;
  cryptocurrency: string;
  trigger_type: string;
  trigger_value: number;
  value: number;
  expires_at: string;
  base_value: number;
}

export interface IAlertProps {
  cryptoPrices: any[];
  onAlertUpdate: (newAlert: any) => void;
  userId: string;
}

export interface IAlertListProps {
  alerts: IAlert[];
  setAlerts: React.Dispatch<React.SetStateAction<IAlert[]>>;
  userId: string;
  cryptoPrices: ICryptoPrice[]
}



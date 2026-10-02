import type { LucideIcon } from 'lucide-react';

export interface NavItem {
  id: string;
  label: string;
  href: string;
  icon: LucideIcon;
  active?: boolean;
}

export interface MetricData {
  label: string;
  value: string;
  subValue?: string;
  change?: string;
  isPositive?: boolean;
  code?: string;
}

export interface SolutionCardData {
  number: string;
  title: string;
  description: string;
  iconName: string;
  capabilities: string[];
}

export interface StepData {
  number: string;
  title: string;
  subtitle: string;
  description: string;
  details: string[];
}

export interface SecurityPillarData {
  title: string;
  subtitle: string;
  description: string;
  badge: string;
}

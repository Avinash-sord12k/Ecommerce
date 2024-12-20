import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getFullUrl(path: string) {
  return `${process.env.NEXT_PUBLIC_BASE_PATH}${path}`;
}

export function calculateDiscountPercent(price: number, discount: number) {
  return 100 - Math.floor(((price - discount) / price) * 100);
}

export function cutWords(str: string, count: number) {
  return str.split(" ").slice(0, count).join(" ");
}

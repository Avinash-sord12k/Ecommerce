export interface Product {
  id: number;
  name: string;
  description: string;
  user_id: number;
  price: number;
  slug: string;
  tags: string;
  discount: number;
  stock: number;
  category_id: number;
  sub_category_ids: number[];
  is_active: boolean;
}

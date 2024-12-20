import React from "react";
import ProductCard from "./product-card";
import { components } from "@/schema";

const ProductList = ({
  products,
}: {
  products: components["schemas"]["PaginatedResponse_ProductResponseModel_"]["items"];
}) => {
  return (
    <div className=" grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {products?.map((product) => (
        <ProductCard key={product?.id} {...product} />
      ))}
    </div>
  );
};

export default ProductList;

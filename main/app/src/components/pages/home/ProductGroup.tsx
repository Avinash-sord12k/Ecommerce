import { HomePageStructure, ProductResponse } from "@/app/(main)/page";
import ProductList from "@/components/shared/product-list";

interface ProductGroupProps extends HomePageStructure {
  products: ProductResponse;
}

function ProductGroup({ description, products, title }: ProductGroupProps) {
  return (
    <section className="py-10 mx-auto container w-full">
      <div className="mb-4 text-center">
        <h4 className="text-2xl font-semibold">{title}</h4>
        <p className="text-lg text-gray-500">{description}</p>
      </div>
      {products && <ProductList products={products.items} />}
    </section>
  );
}

export default ProductGroup;

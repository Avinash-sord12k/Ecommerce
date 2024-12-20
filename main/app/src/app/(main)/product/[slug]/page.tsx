import ImageSlider from "@/components/pages/product/image-slider";
import ProductDetails from "@/components/pages/product/product-details";
import { operations } from "@/schema";
import { API_ENDPOINTS } from "@/store/api/config";
import { headers } from "next/headers";

export type SpecificProduct =
  operations["get_product_by_id_api_v1_product_get_by_id__id__get"]["responses"]["200"]["content"]["application/json"]["items"]["0"];

async function getSingleProductById(
  id: string
): Promise<
  operations["get_product_by_id_api_v1_product_get_by_id__id__get"]["responses"]["200"]["content"]["application/json"]["items"]["0"]
> {
  const headerList = await headers();

  const url = new URL(API_ENDPOINTS.getProductsById, process.env.API_URL);
  // add the route id to the url
  url.pathname = url.pathname + `/${id}`;

  console.log("🚀 ~ url:", url.toString());

  const products = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization:
        headerList.get("Authorization") ??
        "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJlbWFpbCI6InRlc3RlckBnbWFpbC5jb20iLCJleHAiOjE3MzQ3MjI4Njh9.mZmtNbj8hOoiz1QOcaI3MsXKiRc7OSKSbpwk0sapQno",
    },
  }).then((res) => {
    return res.json();
  });
  console.log(products);

  return products;
}

type tParams = Promise<{ slug: string }>;

export default async function ProductSpecificPage(props: { params: tParams }) {
  const { slug } = await props.params;
  const product = await getSingleProductById(slug);
  console.log("🚀 ~ product:", product);
  return (
    <section className="py-10 mx-auto container w-full">
      <div className="grid md:grid-cols-2 items-start px-4 py-6 gap-6 md:gap-12 ">
        {/* Left Section */}
        <ImageSlider />

        {/* Right Section */}
        <ProductDetails product={product} />
      </div>
    </section>
  );
}

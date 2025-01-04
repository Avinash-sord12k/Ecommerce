import ImageSlider from "@/components/pages/product/image-slider";
import ProductDetails from "@/components/pages/product/product-details";
import NotFound from "@/components/shared/not-found";
import { operations } from "@/schema";
import { API_ENDPOINTS } from "@/store/api/config";
import { cookies } from "next/headers";
import { redirect, RedirectType } from "next/navigation";

export type ProductResponse =
  operations["get_products_api_v1_product_get"]["responses"]["200"]["content"]["application/json"];

export type SpecificProduct = ProductResponse["items"]["0"];

async function getSingleProductById(id: string): Promise<SpecificProduct | null> {
  const url = new URL(API_ENDPOINTS.getProducts, process.env.API_URL);
  // add the route id to the url
  url.searchParams.append("id", id);
  const cookieList = await cookies();
  const allCookie = cookieList.getAll();
  if (!allCookie?.length) {
    redirect("/login", RedirectType.replace);
  }

  console.log("🚀 ~ url:", url.toString(), allCookie);

  const products = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      cookie: allCookie.map((cookie) => `${cookie.name}=${cookie.value}`).join("; "),
    },
  }).then((res) => {
    return res.json();
  });
  console.log("products: ", products);

  return products.items[0];
}

type tParams = Promise<{ slug: string }>;

export default async function ProductSpecificPage(props: { params: tParams }) {
  const { slug } = await props.params;
  const product = await getSingleProductById(slug);
  console.log("🚀 ~ ProductSpecificPage ~ item:", product);

  if (!product) return <NotFound />;

  console.log("🚀 ~ product:", product);
  return (
    <section className="py-10 mx-auto container w-full">
      <div className="grid md:grid-cols-2 items-start px-4 py-6 gap-6 md:gap-12 ">
        <ImageSlider images={product?.images ?? []} />
        <ProductDetails product={product} />
      </div>
    </section>
  );
}

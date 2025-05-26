"use client";
import { useRef, useState } from "react"; // useState をインポート
import { useRouter } from "next/navigation";

import createCustomer from "./createCustomer";

export default function CreatePage() {
  const formRef = useRef();
  const router = useRouter();
  // エラーメッセージを管理するためのstateを追加
  const [errors, setErrors] = useState({});

  const validateForm = (formData) => {
    const newErrors = {};
    const customer_name = formData.get("customer_name");
    const customer_id = formData.get("customer_id");
    const age = formData.get("age");
    const gender = formData.get("gender");

    if (!customer_name || customer_name.trim() === "") {
      newErrors.customer_name = "名前を入力してください。";
    }
    if (!customer_id || customer_id.trim() === "") {
      newErrors.customer_id = "Customer IDを入力してください。";
    }
    if (!age || age.trim() === "") {
      // 年齢は数値であるべきですが、ここではまず空かどうかをチェック
      newErrors.age = "年齢を入力してください。";
    } else if (isNaN(parseInt(age, 10))) {
      newErrors.age = "年齢は数値で入力してください。";
    }
    if (!gender || gender.trim() === "") {
      newErrors.gender = "性別を入力してください。";
    }
    return newErrors;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setErrors({}); // 送信試行時に既存のエラーをクリア

    const formData = new FormData(formRef.current);
    const formValidationErrors = validateForm(formData);

    if (Object.keys(formValidationErrors).length > 0) {
      setErrors(formValidationErrors); // 検証エラーがあれば表示
      return; // 送信を中止
    }

    try {
      await createCustomer(formData);
      router.push(`./create/confirm?customer_id=${formData.get("customer_id")}`);
    } catch (error) {
      // createCustomer でエラーがスローされた場合 (例: API接続失敗)
      console.error("Failed to create customer:", error);
      setErrors({ submit: "顧客情報の作成に失敗しました。しばらくしてから再度お試しください。" });
    }
  };

  return (
    <>
      <div className="card bordered bg-white border-blue-200 border-2 max-w-md m-4">
        <div className="m-4 card bordered bg-blue-200 duration-200 hover:border-r-red">
          <form ref={formRef} onSubmit={handleSubmit}>
            <div className="card-body">
              <h2 className="card-title">
                <p>
                  <input
                    type="text"
                    name="customer_name"
                    placeholder="桃太郎"
                    className="input input-bordered w-full" // w-fullを追加して幅を調整
                  />
                  {/* 名前エラーメッセージ表示 */}
                  {errors.customer_name && <span className="text-red-500 text-xs pt-1">{errors.customer_name}</span>}
                </p>
              </h2>
              <p className="mt-2"> {/* 各項目間のマージン調整 */}
                Customer ID:
                <input
                  type="text"
                  name="customer_id"
                  placeholder="C030"
                  className="input input-bordered w-full mt-1" // w-fullとmt-1を追加
                />
                {/* Customer IDエラーメッセージ表示 */}
                {errors.customer_id && <span className="text-red-500 text-xs pt-1">{errors.customer_id}</span>}
              </p>
              <p className="mt-2">
                Age:
                <input
                  type="number" // type="text" から "number" に変更が適切だが、検証ロジックで数値チェックも入れている
                  name="age"
                  placeholder="30"
                  className="input input-bordered w-full mt-1"
                />
                {/* 年齢エラーメッセージ表示 */}
                {errors.age && <span className="text-red-500 text-xs pt-1">{errors.age}</span>}
              </p>
              <p className="mt-2">
                Gender:
                <input
                  type="text"
                  name="gender"
                  placeholder="女"
                  className="input input-bordered w-full mt-1"
                />
                {/* 性別エラーメッセージ表示 */}
                {errors.gender && <span className="text-red-500 text-xs pt-1">{errors.gender}</span>}
              </p>
              {/* フォーム全体に関するエラーメッセージ (例: 送信失敗時) */}
              {errors.submit && <p className="text-red-500 text-xs pt-2">{errors.submit}</p>}
            </div>
            <div className="flex justify-center">
              <button type="submit" className="btn btn-primary m-4 text-2xl">
                作成
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}
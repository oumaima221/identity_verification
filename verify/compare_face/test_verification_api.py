import base64
import requests
import json

CONFIG = {
    "server_url": "http://localhost:8000",
    "api_keys": {
        "detection": "3b570619-a3c5-4d46-bb78-a1e7d3d0dfe6",
        "recognition": "e4f8cbfa-3585-4eb8-a6ef-5e068d083c20",
        "verification": "05476a69-db31-4539-88b1-d2e8bbf4dcba"
    },
    "endpoints": {
        "detection": "/api/v1/detection/detect",
        "recognition": "/api/v1/recognition/recognize",
        "verification": "/api/v1/verification/verify"
    }
}

def encode_image(image_path):
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
            if not image_data:
                print("Error: Empty image file")
                return None
            return base64.b64encode(image_data).decode('utf-8')
    except Exception as e:
        print(f"Image encoding error: {str(e)}")
        return None

def make_api_request(service, payload):
    try:
        url = f"{CONFIG['server_url']}{CONFIG['endpoints'][service]}"
        headers = {
            "x-api-key": CONFIG['api_keys'][service],
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"API Error ({service}): {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                print(f"Error details: {json.dumps(error_details, indent=2)}")
            except:
                print(f"Raw response: {e.response.text}")
        return None

def test_all_apis(source_image_path, target_image_path):
    source_b64 = encode_image(source_image_path)
    target_b64 = encode_image(target_image_path)
    if not source_b64 or not target_b64:
        print("Failed to encode images")
        return

    # Validate source image contains face
    detection_source = make_api_request("detection", {"file": source_b64})
    if not detection_source or not detection_source.get("result"):
        print("Face detection failed on source image")
        return
    print("Detection source result:", json.dumps(detection_source, indent=2))

    # Validate target image contains face
    detection_target = make_api_request("detection", {"file": target_b64})
    if not detection_target or not detection_target.get("result"):
        print("Face detection failed on target image")
        return
    print("Detection target result:", json.dumps(detection_target, indent=2))

    # Face recognition on source image
    recognition_source = make_api_request("recognition", {"file": source_b64})
    if not recognition_source:
        print("Face recognition failed on source image")
        return
    print("Recognition source result:", json.dumps(recognition_source, indent=2))

    # Face recognition on target image
    recognition_target = make_api_request("recognition", {"file": target_b64})
    if not recognition_target:
        print("Face recognition failed on target image")
        return
    print("Recognition target result:", json.dumps(recognition_target, indent=2))

    # Verification
    verification = make_api_request("verification", {
        "source_image": source_b64,
        "target_image": target_b64
    })
    if not verification or not verification.get("result"):
        print("Face verification failed")
        return
    print("Verification result:", json.dumps(verification, indent=2))

if __name__ == "__main__":
    test_all_apis(
        "/home/oumayma/identity_verification/media/temp/image1.19.png",
        "/home/oumayma/identity_verification/verify/compare_face/captured_target_face.jpg"
    )


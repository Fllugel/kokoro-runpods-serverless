#!/usr/bin/env python3
"""
Comprehensive test script for the Kokoro FastAPI Serverless Wrapper
Tests all endpoints from the original API schema
"""

import base64
import json
import time

# Import the wrapper handler
from handler_wrapper import handler

def test_wrapper():
    """Test all wrapper handler endpoints"""

    print("Testing Kokoro FastAPI Serverless Wrapper - ALL ENDPOINTS")
    print("=" * 60)

    # Wait a bit for FastAPI to start
    print("Waiting for FastAPI to start...")
    time.sleep(10)

    # Test cases covering all endpoints
    test_cases = [
        {
            "name": "TTS - OpenAI-compatible format",
            "input": {
                "model": "kokoro",
                "input": "Hello, this is a test using the wrapper approach.",
                "voice": "af_bella",
                "response_format": "mp3",
                "speed": 1.0
            }
        },
        {
            "name": "TTS - Simple format",
            "input": {
                "text": "Testing simple format with the wrapper.",
                "voice": "af_bella",
                "format": "wav",
                "speed": 1.2
            }
        },
        {
            "name": "TTS - Voice combination",
            "input": {
                "model": "kokoro",
                "input": "Testing voice combinations.",
                "voice": "af_bella+af_sky",
                "response_format": "mp3"
            }
        },
        {
            "name": "List Voices",
            "input": {
                "endpoint": "/v1/audio/voices",
                "method": "GET"
            }
        },
        {
            "name": "List Models",
            "input": {
                "endpoint": "/v1/models",
                "method": "GET"
            }
        },
        {
            "name": "Phonemize Text",
            "input": {
                "endpoint": "/dev/phonemize",
                "method": "POST",
                "text": "Hello world, this is a phonemization test.",
                "language": "a"
            }
        },
        {
            "name": "Captioned Speech (with timestamps)",
            "input": {
                "endpoint": "/dev/captioned_speech",
                "method": "POST",
                "input": "This is a test for captioned speech with word timestamps.",
                "voice": "af_bella",
                "response_format": "mp3",
                "return_timestamps": True
            }
        },
        {
            "name": "Voice Combination",
            "input": {
                "endpoint": "/v1/audio/voices/combine",
                "method": "POST",
                "voices": "af_bella+af_sky"
            }
        }
    ]

    results = []

    # Run test cases
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        print("-" * 40)

        # Create job payload
        job = {"input": test_case["input"]}

        try:
            result = handler(job)

            if result.get("success"):
                print("✓ Request successful")

                # Handle different response types
                if "audio_base64" in result:
                    print(f"  Voice: {result.get('voice', 'N/A')}")
                    print(f"  Speed: {result.get('speed', 'N/A')}")
                    print(f"  Format: {result.get('format', 'N/A')}")
                    print(f"  Model: {result.get('model', 'N/A')}")
                    print(f"  Audio size: {result.get('size_bytes', 0)} bytes")

                    # Save audio file for testing
                    audio_data = base64.b64decode(result["audio_base64"])
                    format_ext = result.get('format', 'mp3')
                    filename = f"test_{i}_{test_case['name'].lower().replace(' ', '_').replace('-', '').replace('(', '').replace(')', '')}.{format_ext}"
                    with open(filename, "wb") as f:
                        f.write(audio_data)
                    print(f"  Audio saved as: {filename}")

                elif "voices" in result:
                    voices = result["voices"]
                    print(f"  Found {len(voices)} voices")
                    print(f"  Sample voices: {voices[:3] if len(voices) > 3 else voices}")

                elif "models" in result:
                    models = result["models"]
                    print(f"  Models response: {models}")

                elif "result" in result:
                    res = result["result"]
                    if "phonemes" in res:
                        print(f"  Phonemes: {res['phonemes'][:50]}...")
                        print(f"  Tokens count: {len(res.get('tokens', []))}")
                    elif "audio" in res:
                        print(f"  Captioned speech with audio and timestamps")
                        if "timestamps" in res:
                            print(f"  Timestamp count: {len(res['timestamps'])}")
                    else:
                        print(f"  Result: {str(res)[:100]}...")

                elif "voice_file_base64" in result:
                    print(f"  Voice combination successful")
                    print(f"  Combined voices: {result.get('voices', 'N/A')}")
                    print(f"  File size: {result.get('size_bytes', 0)} bytes")

                    # Save voice file
                    file_data = base64.b64decode(result["voice_file_base64"])
                    filename = f"combined_voice_{i}.pt"
                    with open(filename, "wb") as f:
                        f.write(file_data)
                    print(f"  Voice file saved as: {filename}")

                results.append({"test": test_case["name"], "status": "PASS"})

            else:
                print(f"✗ Request failed: {result.get('error', 'Unknown error')}")
                results.append({"test": test_case["name"], "status": "FAIL", "error": result.get('error')})

        except Exception as e:
            print(f"✗ Exception occurred: {e}")
            results.append({"test": test_case["name"], "status": "ERROR", "error": str(e)})

        print()

    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = len([r for r in results if r["status"] == "PASS"])
    failed = len([r for r in results if r["status"] in ["FAIL", "ERROR"]])

    print(f"Total tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()

    for result in results:
        status_icon = "✓" if result["status"] == "PASS" else "✗"
        print(f"{status_icon} {result['test']}: {result['status']}")
        if "error" in result:
            print(f"    Error: {result['error']}")

    print("\nWrapper testing complete!")

    if failed == 0:
        print("🎉 ALL TESTS PASSED - Wrapper is ready for deployment!")
    else:
        print(f"⚠️  {failed} test(s) failed - review errors above")

if __name__ == "__main__":
    test_wrapper()
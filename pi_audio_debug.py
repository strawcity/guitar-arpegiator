#!/usr/bin/env python3
"""
Raspberry Pi Audio Debug Script

Run this on your Pi to diagnose why the effects aren't working.
This will test each component step by step.
"""

import sys
import time
import numpy as np

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import sounddevice as sd
        print("✅ sounddevice imported")
    except Exception as e:
        print(f"❌ sounddevice import failed: {e}")
        return False
        
    try:
        from config import Config
        print("✅ config imported")
    except Exception as e:
        print(f"❌ config import failed: {e}")
        return False
        
    try:
        from optimized_audio_processor import OptimizedAudioProcessor
        print("✅ OptimizedAudioProcessor imported")
    except Exception as e:
        print(f"❌ OptimizedAudioProcessor import failed: {e}")
        return False
        from optimized_audio_processor import OptimizedAudioProcessor
        print("✅ OptimizedAudioProcessor imported")
    except Exception as e:
        print(f"❌ OptimizedAudioProcessor import failed: {e}")
        return False
        
    return True

def test_audio_devices():
    """Test audio device detection."""
    print("\n🎧 Testing audio devices...")
    
    try:
        import sounddevice as sd
        
        devices = sd.query_devices()
        print(f"Found {len(devices)} audio devices:")
        
        for i, device in enumerate(devices):
            print(f"  {i}: {device['name']}")
            print(f"     Input channels: {device['max_inputs']}")
            print(f"     Output channels: {device['max_outputs']}")
            print(f"     Default sample rate: {device['default_samplerate']}")
            
        # Find Scarlett 2i2
        scarlett_devices = [d for d in devices if 'scarlett' in d['name'].lower() or '2i2' in d['name'].lower()]
        if scarlett_devices:
            print(f"\n✅ Found Scarlett 2i2: {scarlett_devices[0]['name']}")
        else:
            print("\n⚠️  Scarlett 2i2 not found - check USB connection")
            
        return True
        
    except Exception as e:
        print(f"❌ Audio device test failed: {e}")
        return False

def test_basic_audio():
    """Test basic audio input/output."""
    print("\n🔊 Testing basic audio...")
    
    try:
        import sounddevice as sd
        
        # Test simple audio output
        print("Testing audio output...")
        sample_rate = 48000
        duration = 1.0
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        test_tone = 0.3 * np.sin(2 * np.pi * 440 * t)  # 440Hz A note
        
        sd.play(test_tone, sample_rate)
        sd.wait()
        print("✅ Audio output test passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic audio test failed: {e}")
        return False

def test_config():
    """Test configuration system."""
    print("\n⚙️  Testing configuration...")
    
    try:
        from config import Config
        
        config = Config()
        print(f"✅ Config loaded")
        print(f"   Platform: {'Pi' if config.is_pi else 'Other'}")
        print(f"   Sample rate: {config.sample_rate}")
        print(f"   Chunk size: {config.chunk_size}")
        print(f"   Default tempo: {config.default_tempo}")
        
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False





def test_audio_processor():
    """Test audio processor."""
    print("\n🎵 Testing audio processor...")
    
    try:
        from optimized_audio_processor import OptimizedAudioProcessor
        from config import Config
        
        config = Config()
        processor = OptimizedAudioProcessor(config)
        print("✅ OptimizedAudioProcessor initialized")
        
        # Test status
        status = processor.get_status()
        print(f"   Buffer size: {status['buffer_size']}")
        print(f"   Sample rate: {status['sample_rate']}")
        print(f"   Active effects: {status['active_effects']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Audio processor test failed: {e}")
        return False

def test_audio_stream():
    """Test audio stream creation."""
    print("\n🌊 Testing audio stream...")
    
    try:
        import sounddevice as sd
        
        # Test input stream
        print("Testing input stream...")
        with sd.InputStream(
            channels=1,
            samplerate=48000,
            blocksize=1024,
            dtype=np.float32,
            latency='high'
        ) as stream:
            print("✅ Input stream created successfully")
            
        # Test output stream
        print("Testing output stream...")
        with sd.OutputStream(
            channels=1,
            samplerate=48000,
            blocksize=1024,
            dtype=np.float32,
            latency='high'
        ) as stream:
            print("✅ Output stream created successfully")
            
        return True
        
    except Exception as e:
        print(f"❌ Audio stream test failed: {e}")
        return False

def main():
    """Run all diagnostic tests."""
    print("🔍 RASPBERRY PI AUDIO DIAGNOSTICS")
    print("=" * 60)
    print("This script will test each component to find the issue")
    print("Run this on your Pi with the Scarlett 2i2 connected")
    print()
    
    tests = [
        ("Imports", test_imports),
        ("Audio Devices", test_audio_devices),
        ("Basic Audio", test_basic_audio),
        ("Configuration", test_config),


        ("Audio Processor", test_audio_processor),
        ("Audio Streams", test_audio_stream),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system should work.")
        print("💡 If effects still don't work, try the interactive CLI:")
        print("   python3 interactive_cli.py")
    else:
        print("❌ Some tests failed. Check the errors above.")
        print("💡 Common issues:")
        print("   - USB audio interface not connected")
        print("   - ALSA configuration problems")
        print("   - Permission issues")
        print("   - Run: python3 fix_pi_audio.py --fix")

if __name__ == "__main__":
    main()

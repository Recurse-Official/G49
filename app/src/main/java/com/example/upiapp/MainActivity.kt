package com.example.upiapp


import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import com.google.zxing.integration.android.IntentIntegrator
import com.google.zxing.integration.android.IntentResult

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Reference the button
        val scanButton: Button = findViewById(R.id.btn_scan)

        // Set click listener for scanning
        scanButton.setOnClickListener {
            IntentIntegrator(this)
                .setCaptureActivity(CaptureActivity::class.java)
                .initiateScan()
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        // Handle the scanning result
        val result: IntentResult? = IntentIntegrator.parseActivityResult(requestCode, resultCode, data)
        if (result != null && result.contents != null) {
            val upiString = result.contents // Extract UPI QR code string
            initiateUPIPayment(upiString)
        }
    }

    private fun initiateUPIPayment(upiString: String) {
        val intent = Intent(Intent.ACTION_VIEW).apply {
            data = Uri.parse(upiString) // Use the scanned UPI string
        }
        val chooser = Intent.createChooser(intent, "Pay with...")
        startActivity(chooser)
    }
}


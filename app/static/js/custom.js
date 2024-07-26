//fade scroll effect
AOS.init();
// Fungsi
var ID = function(elID) {
    return document.getElementById(elID);
};

var hide = function(id) {
    return id.classList.add("d-none");
};

var show = function(id) {
    return id.classList.remove("d-none");
};

var inHtm = function(el, content) {
    return (el.innerHTML = content);
};

// Akhir Fungsi

// Deklarasi semua variabel
// yang dibutuhkan menggunakan id elemen
var emptyTraining = ID("trainkosong");
var emptyPrediksi = ID("testkosong");
var emptyRealtime = ID("realtime-kosong");

var btnTrainReset = ID("btnTrainReset");
var btnTestReset = ID("btnTestReset");
var btnTrain = ID("btnTraining");
var btnTest = ID("btnTest");
var btnTestResetrt = ID("btnTestResetrt");
var btnTestrt = ID("btnTestrt");


var spinner = ID("spinner");
var testSpinner = ID("test_spinner");
var testSpinner_rt = ID("test_spinner_rt");
var hasilTestRealTime = ID("hasilTestRealTime");

var hasilTraining = ID("hasilTraining");
var hasilTest = ID("hasilTest")



var formTrain = ID("formTrain");
var formTest = ID("formTest");
var formTestRealTime = ID("formTestRealTime");

//testDataset
var hm = ID("hm");
var ch = ID("ch");
var testRealtime = ID('test-realtime');
var kalimatPred = ID('kalimat-pred');
var hargaPred = ID('harga-pred');
var kebersihanPred = ID('kebersihan-pred');
var pelayananPred = ID('pelayanan-pred');
var lokasiPred = ID('lokasi-pred');
var fasilitasPred = ID('fasilitas-pred');


var hm_harga = ID("hm_harga");
var hm_kebersihan = ID("hm_kebersihan");
var hm_pelayanan = ID("hm_pelayanan");
var hm_lokasi = ID("hm_lokasi");
var hm_kebersihan = ID("hm_kebersihan");

var harga_ga = ID("harga_ga");
var kebersihan_ga = ID("kebersihan_ga");
var pelayanan_ga = ID("pelayanan_ga");
var lokasi_ga = ID("lokasi_ga");
var fasilitas_ga = ID("fasilitas_ga");

var harga_gl = ID("harga_gl");
var kebersihan_gl = ID("kebersihan_gl");
var pelayanan_gl = ID("pelayanan_gl");
var lokasi_gl = ID("lokasi_gl");
var fasilitas_gl = ID("fasilitas_gl");

var hist_harga = ID("hist_harga");
var hist_kebersihan = ID("hist_kebersihan");
var hist_pelayanan = ID("hist_pelayanan");
var hist_lokasi = ID("hist_lokasi");
var hist_fasilitas = ID("hist_fasilitas");



// Akhir Deklarasi Variabel

//! Train
// eslint-disable-next-line no-undef
$(formTrain).submit(function(e) {
    e.preventDefault();
    show(emptyTraining);
    hide(hasilTraining);
    hide(btnTrain);

    show(btnTrainReset);
    show(spinner);

    var formData = new FormData(this);
    // eslint-disable-next-line no-undef
    var xhr = $.ajax({
        url: "/train",
        type: "POST",
        cache: false,
        contentType: false,
        processData: false,
        data: formData,
        success: function(data) {
            // eslint-disable-next-line no-undef
            obj = $.parseJSON(data);

            hide(spinner);
            hide(emptyTraining);
            show(hasilTraining);
            show(hasilGraph);

            setupDataPreproses();

            $(harga_ga).attr("src", "./static/img/grafik/" + obj["harga_ga"]);
            $(kebersihan_ga).attr("src", "./static/img/grafik/" + obj["kebersihan_ga"]);
            $(pelayanan_ga).attr("src", "./static/img/grafik/" + obj["pelayanan_ga"]);
            $(lokasi_ga).attr("src", "./static/img/grafik/" + obj["lokasi_ga"]);
            $(fasilitas_ga).attr("src", "./static/img/grafik/" + obj["fasilitas_ga"]);
            $(harga_gl).attr("src", "./static/img/grafik/" + obj["harga_gl"]);
            $(kebersihan_gl).attr("src", "./static/img/grafik/" + obj["kebersihan_gl"]);
            $(pelayanan_gl).attr("src", "./static/img/grafik/" + obj["pelayanan_gl"]);
            $(lokasi_gl).attr("src", "./static/img/grafik/" + obj["lokasi_gl"]);
            $(fasilitas_gl).attr("src", "./static/img/grafik/" + obj["fasilitas_gl"]);


            console.log(obj["message"]);

            console.log(obj["hPrep"]);

        },
        error: function(xhr, ajaxOption, thrownError) {
            // eslint-disable-next-line no-undef
            Swal.fire({
                icon: "error",
                title: "Proses Dibatalkan",
                confirmButtonColor: "#577EF4",
            });
            location.reload();
        },
    });

    btnTrainReset.onclick = function() {
        xhr.abort();
        $(formTrain)[0].reset();
        hide(btnTrainReset);
        show(btnTrain);
    };
});
//? Akhir Proses Train

//! Akhir Train

//! Get Hasil Prediksi
function setupDataPreproses() {

    $('#tbPrep').DataTable({
        "destroy": true,
        "ajax": {
            "url": '/hpreproses',
            "dataType": "json",
            "dataSrc": "data",
            "contentType": "application/json"
        },
        "columns": [{
                "data": "Nama Hotel"
            },
            {
                "data": "Nama"
            },
            {
                "data": "Ulasan"
            },
            {
                "data": "Preprocess"
            },
            {
                "data": "Harga"
            },
            {
                "data": "Kebersihan"
            },
            {
                "data": "Pelayanan"
            },
            {
                "data": "Lokasi"
            },
            {
                "data": "Fasilitas"
            }
        ],

        "columnDefs": [{
                "className": "bolded",
                "targets": -1
            },
            {
                "className": "text-left",
                "targets": "_all"
            },
        ],
    });

}
//! END Hasil Prediksi

// Get Table Result
function setupDataResult() {

    $('#tbResult').DataTable({
        "destroy": true,
        "ajax": {
            "url": '/hpResult',
            "dataType": "json",
            "dataSrc": "data",
            "contentType": "application/json"
        },
        "columns": [{
                "data": "Nama Hotel"
            },
            {
                "data": "Nama"
            },
            {
                "data": "Ulasan"
            },
            {
                "data": "Preprocess"
            },
            // {
            //   "data": "Harga"
            // },
            // {
            //   "data": "Kebersihan"
            // },
            // {
            //   "data": "Pelayanan"
            // },
            // {
            //   "data": "Lokasi"
            // },
            // {
            //   "data": "Fasilitas"
            // },
            {
                "data": "harga_pred"
            },
            {
                "data": "kebersihan_pred"
            },
            {
                "data": "pelayanan_pred"
            },
            {
                "data": "lokasi_pred"
            },
            {
                "data": "fasilitas_pred"
            }
        ],

        "columnDefs": [{
                "className": "text-left",
                "targets": 0
            },
            {
                "className": "text-center",
                "targets": "_all"
            },
        ],
    });
}
// END TABLE RESULT
setupDataReport();
// GET TABLE REPORT
function setupDataReport() {

    $('#tbReportHarga').DataTable({
        "destroy": true,
        "ajax": {
            "url": '/hpReportHarga',
            "dataType": "json",
            "dataSrc": "data",
            "contentType": "application/json"
        },
        "columns": [{
                "data": "index"
            },
            {
                "data": "precision"
            },
            {
                "data": "recall"
            },
            {
                "data": "f1-score"
            },
            {
                "data": "support"
            }
        ],

        "columnDefs": [{
                "className": "text-left",
                "targets": 0
            },
            {
                "className": "text-center",
                "targets": "_all"
            },
        ],
        "paging": false,
        "ordering": false,
        "info": false,
        "searching": false
    });


    $('#tbReportKebersihan').DataTable({
        "destroy": true,
        "ajax": {
            "url": '/hpReportKebersihan',
            "dataType": "json",
            "dataSrc": "data",
            "contentType": "application/json"
        },
        "columns": [{
                "data": "index"
            },
            {
                "data": "precision"
            },
            {
                "data": "recall"
            },
            {
                "data": "f1-score"
            },
            {
                "data": "support"
            }
        ],

        "columnDefs": [{
                "className": "text-left",
                "targets": 0
            },
            {
                "className": "text-center",
                "targets": "_all"
            },
        ],
        "paging": false,
        "ordering": false,
        "info": false,
        "searching": false
    });



    $('#tbReportPelayanan').DataTable({
        "destroy": true,
        "ajax": {
            "url": '/hpReportPelayanan',
            "dataType": "json",
            "dataSrc": "data",
            "contentType": "application/json"
        },
        "columns": [{
                "data": "index"
            },
            {
                "data": "precision"
            },
            {
                "data": "recall"
            },
            {
                "data": "f1-score"
            },
            {
                "data": "support"
            }
        ],

        "columnDefs": [{
                "className": "text-left",
                "targets": 0
            },
            {
                "className": "text-center",
                "targets": "_all"
            },
        ],
        "paging": false,
        "ordering": false,
        "info": false,
        "searching": false
    });


    $('#tbReportLokasi').DataTable({
        "destroy": true,
        "ajax": {
            "url": '/hpReportLokasi',
            "dataType": "json",
            "dataSrc": "data",
            "contentType": "application/json"
        },
        "columns": [{
                "data": "index"
            },
            {
                "data": "precision"
            },
            {
                "data": "recall"
            },
            {
                "data": "f1-score"
            },
            {
                "data": "support"
            }
        ],

        "columnDefs": [{
                "className": "text-left",
                "targets": 0
            },
            {
                "className": "text-center",
                "targets": "_all"
            },
        ],
        "paging": false,
        "ordering": false,
        "info": false,
        "searching": false
    });


    $('#tbReportFasilitas').DataTable({
        "destroy": true,
        "ajax": {
            "url": '/hpReportFasilitas',
            "dataType": "json",
            "dataSrc": "data",
            "contentType": "application/json"
        },
        "columns": [{
                "data": "index"
            },
            {
                "data": "precision"
            },
            {
                "data": "recall"
            },
            {
                "data": "f1-score"
            },
            {
                "data": "support"
            }
        ],

        "columnDefs": [{
                "className": "text-left",
                "targets": 0
            },
            {
                "className": "text-center",
                "targets": "_all"
            },
        ],
        "paging": false,
        "ordering": false,
        "info": false,
        "searching": false
    });

    //////////////////////////////////////////////////////////

    $('#tb-Harga').DataTable({
        "destroy": true,
        "ajax": {
            "url": '/hpTBHarga',
            "dataType": "json",
            "dataSrc": "data",
            "contentType": "application/json"
        },
        "columns": [
            {
                "data": "Nama Hotel"
            },
            {
                "data": "-1"
            },
            {
                "data": "1"
            }
        ],

        "columnDefs": [{
                "className": "text-left",
                "targets": 0
            },
            {
                "className": "text-center",
                "targets": "_all"
            },
        ],
        "paging": false,
        "ordering": false,
        "info": false,
        "searching": false
    });

    $('#tb-Kebersihan').DataTable({
        "destroy": true,
        "ajax": {
            "url": '/hpTBKebersihan',
            "dataType": "json",
            "dataSrc": "data",
            "contentType": "application/json"
        },
        "columns": [
            {
                "data": "Nama Hotel"
            },
            {
                "data": "-1"
            },
            {
                "data": "1"
            }
        ],

        "columnDefs": [{
                "className": "text-left",
                "targets": 0
            },
            {
                "className": "text-center",
                "targets": "_all"
            },
        ],
        "paging": false,
        "ordering": false,
        "info": false,
        "searching": false
    });

    $('#tb-Pelayanan').DataTable({
        "destroy": true,
        "ajax": {
            "url": '/hpTBPelayanan',
            "dataType": "json",
            "dataSrc": "data",
            "contentType": "application/json"
        },
        "columns": [
            {
                "data": "Nama Hotel"
            },
            {
                "data": "-1"
            },
            {
                "data": "1"
            }
        ],

        "columnDefs": [{
                "className": "text-left",
                "targets": 0
            },
            {
                "className": "text-center",
                "targets": "_all"
            },
        ],
        "paging": false,
        "ordering": false,
        "info": false,
        "searching": false
    });

    $('#tb-Lokasi').DataTable({
        "destroy": true,
        "ajax": {
            "url": '/hpTBLokasi',
            "dataType": "json",
            "dataSrc": "data",
            "contentType": "application/json"
        },
        "columns": [
            {
                "data": "Nama Hotel"
            },
            {
                "data": "-1"
            },
            {
                "data": "1"
            }
        ],

        "columnDefs": [{
                "className": "text-left",
                "targets": 0
            },
            {
                "className": "text-center",
                "targets": "_all"
            },
        ],
        "paging": false,
        "ordering": false,
        "info": false,
        "searching": false
    });

    $('#tb-Fasilitas').DataTable({
        "destroy": true,
        "ajax": {
            "url": '/hpTBFasilitas',
            "dataType": "json",
            "dataSrc": "data",
            "contentType": "application/json"
        },
        "columns": [
            {
                "data": "Nama Hotel"
            },
            {
                "data": "-1"
            },
            {
                "data": "1"
            }
        ],

        "columnDefs": [{
                "className": "text-left",
                "targets": 0
            },
            {
                "className": "text-center",
                "targets": "_all"
            },
        ],
        "paging": false,
        "ordering": false,
        "info": false,
        "searching": false
    });

}
// END TABLE REPORT

//! Test
// eslint-disable-next-line no-undef
$(formTest).submit(function(e) {
    e.preventDefault();

    show(emptyPrediksi);
    hide(btnTest);
    hide(hasilTest);

    show(btnTestReset);
    show(testSpinner);
    var formData = new FormData(this);
    // eslint-disable-next-line no-undef
    var xhr = $.ajax({
        url: "/test",
        type: "POST",
        cache: false,
        contentType: false,
        processData: false,
        data: formData,
        success: function(data) {
            // eslint-disable-next-line no-undef
            obj = $.parseJSON(data);
            $(hm_harga).attr("src", "./static/img/grafik/" + obj["hm_harga"]);
            $(hm_kebersihan).attr("src", "./static/img/grafik/" + obj["hm_kebersihan"]);
            $(hm_pelayanan).attr("src", "./static/img/grafik/" + obj["hm_pelayanan"]);
            $(hm_lokasi).attr("src", "./static/img/grafik/" + obj["hm_lokasi"]);
            $(hm_fasilitas).attr("src", "./static/img/grafik/" + obj["hm_fasilitas"]);

            $(hist_harga).attr("src", "./static/img/grafik/" + obj["hist_harga"]);
            $(hist_kebersihan).attr("src", "./static/img/grafik/" + obj["hist_kebersihan"]);
            $(hist_pelayanan).attr("src", "./static/img/grafik/" + obj["hist_pelayanan"]);
            $(hist_lokasi).attr("src", "./static/img/grafik/" + obj["hist_lokasi"]);
            $(hist_fasilitas).attr("src", "./static/img/grafik/" + obj["hist_fasilitas"]);

            hide(testSpinner);
            hide(emptyPrediksi);
            show(hasilTest);
            setupDataResult();
            setupDataReport();
        },
        error: function(xhr, ajaxOption, thrownError) {
            // eslint-disable-next-line no-undef
            Swal.fire({
                icon: "error",
                title: 'Terjadi Masalah :(',
                text: 'Periksa Server',
                confirmButtonText: `Oke`
            }).then((result) => {
                if (result.isConfirmed) {
                    location.reload();
                }
            })
        },
    });

    btnTestReset.onclick = function() {
        xhr.abort();
        $(formTest)[0].reset();
        hide(btnTestReset);
        show(btnTest);
    };

});
//! Akhir Test

$(formTestRealTime).submit(function (e) {
    e.preventDefault();
  
    show(emptyRealtime);
    hide(btnTestrt);
    hide(hasilTestRealTime);
  
    show(btnTestResetrt);
    show(testSpinner_rt);
    var formData = new FormData(this);
    // eslint-disable-next-line no-undef
    var xhr = $.ajax({
      url: "/realtimetext",
      type: "POST",
      cache: false,
      contentType: false,
      processData: false,
      data: formData,
      success: function (data) {
          // eslint-disable-next-line no-undef
          obj = $.parseJSON(data);
  
          inHtm(kalimatPred, obj["kalimat_pred"])
          inHtm(hargaPred, obj["harga_pred"])
          inHtm(kebersihanPred, obj["kebersihan_pred"])
          inHtm(pelayananPred, obj["pelayanan_pred"])
          inHtm(lokasiPred, obj["lokasi_pred"])
          inHtm(fasilitasPred, obj["fasilitas_pred"])
          hide(testSpinner_rt);
          hide(emptyRealtime);
          show(hasilTestRealTime);
      },
      // success: function (data) {
      //   // eslint-disable-next-line no-undef
      //   obj = $.parseJSON(data);
      //   console.log(obj["prediction"]);
      //   // 
      //   hide(testSpinner);
      //   hide(emptyPrediksi);
      //   show(hasilTestRealTime);
      //   setupDataResult();
      //   setupDataReport();
      // },
      error: function (xhr, ajaxOption, thrownError) {
        // eslint-disable-next-line no-undef
        Swal.fire({
          icon: "error",
          title: 'Terjadi Masalah :(',
          text: 'Periksa Server',
          confirmButtonText: `Oke`
        }).then((result) => {
          if (result.isConfirmed) {
            location.reload();
          }
        })
      },
    });
  
    btnTestResetrt.onclick = function () {
      xhr.abort();
      $(formTestRealTime)[0].reset();
      hide(btnTestResetrt);
      show(btnTestrt);
    };
  
  });


window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function() {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function(responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    // // Activate SimpleLightbox plugin for portfolio items
    // new SimpleLightbox({
    //     elements: '#portfolio a.portfolio-box'
    // });

});
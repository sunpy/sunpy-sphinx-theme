window.onload = async function () {
  const res = await fetch("https://pypi.org/pypi/sunpy/json");
  const data = await res.json();
  document.getElementById("version").innerHTML = data.info.version;
};

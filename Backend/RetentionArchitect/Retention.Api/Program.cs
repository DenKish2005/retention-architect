using Retention.Api.Extensions;
using Retention.Api.Models.Config;

var builder = WebApplication.CreateBuilder(args);

builder.Services.Configure<MlServiceOptions>(
    builder.Configuration.GetSection("MlService"));

builder.Services.AddApplicationServices();
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// Serve the frontend from wwwroot/index.html
app.UseDefaultFiles();
app.UseStaticFiles();

app.UseAuthorization();
app.MapControllers();

// Optional: if someone goes to an unknown non-API route,
// return the frontend so the app still feels cohesive.
app.MapFallbackToFile("index.html");

await app.RunAsync();

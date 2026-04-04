using Retention.Api.Models.Config;
using Retention.Api.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.Configure<MlServiceOptions>(
    builder.Configuration.GetSection("MlService"));

builder.Services.AddHttpClient<MlServiceClient>();

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
app.UseAuthorization();
app.MapControllers();

await app.RunAsync();